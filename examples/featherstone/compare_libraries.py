"""The same rotating frame, queried through MuJoCo and Pinocchio.

Run: python examples/featherstone/compare_libraries.py
No viewer, time integration, contacts, or gravity. All printed six-vectors use
[angular; linear]; Pinocchio's raw .vector uses the opposite ordering.
"""

import argparse
import json
import platform
from pathlib import Path

import mujoco
import numpy as np
import pinocchio as pin


def make_models():
    """One z-axis hinge at O, and an attached frame P one metre away."""
    mj_model = mujoco.MjModel.from_xml_string("""
    <mujoco model="rotating-frame">
      <option gravity="0 0 0"/>
      <worldbody>
        <body name="disk">
          <joint name="hinge" type="hinge" axis="0 0 1"/>
          <geom type="cylinder" size="1.2 0.04" mass="1"
                contype="0" conaffinity="0"/>
          <site name="P" pos="1 0 0" size="0.02"/>
        </body>
      </worldbody>
    </mujoco>
    """)
    mj_data = mujoco.MjData(mj_model)
    site_id = mj_model.site("P").id

    pin_model = pin.Model()
    joint_id = pin_model.addJoint(
        0, pin.JointModelRZ(), pin.SE3.Identity(), "hinge"
    )
    frame_id = pin_model.addFrame(pin.Frame(
        "P", joint_id,
        pin.SE3(np.eye(3), np.array([1.0, 0.0, 0.0])),
        pin.FrameType.OP_FRAME,
    ))
    # Only kinematics is queried from Pinocchio, so no inertia is needed.
    return (mj_model, mj_data, site_id), (
        pin_model, pin_model.createData(), frame_id
    )


def angular_first(motion):
    return np.concatenate((motion.angular, motion.linear))


def sample(models, angle, speed=1.0, angular_acceleration=0.0):
    """Evaluate both libraries at the same prescribed q, qdot, qddot."""
    (mj_model, mj_data, site_id), (model, data, frame_id) = models
    mj_data.qpos[:] = angle
    mj_data.qvel[:] = speed
    mj_data.qacc[:] = angular_acceleration
    # Inverse dynamics accepts prescribed qacc; no integration is involved.
    mujoco.mj_inverse(mj_model, mj_data)
    # Required before querying object acceleration in this sensor-free model.
    mujoco.mj_rnePostConstraint(mj_model, mj_data)
    mj_v, mj_a = np.zeros(6), np.zeros(6)
    # SITE pins down the query point, avoiding BODY versus XBODY/COM ambiguity.
    mujoco.mj_objectVelocity(
        mj_model, mj_data, mujoco.mjtObj.mjOBJ_SITE, site_id, mj_v, 0
    )
    mujoco.mj_objectAcceleration(
        mj_model, mj_data, mujoco.mjtObj.mjOBJ_SITE, site_id, mj_a, 0
    )

    q, v, a = np.array([angle]), np.array([speed]), np.array([angular_acceleration])
    pin.forwardKinematics(model, data, q, v, a)
    pin.updateFramePlacements(model, data)
    world, lwa = pin.ReferenceFrame.WORLD, pin.ReferenceFrame.LOCAL_WORLD_ALIGNED
    return {
        "position_mujoco": mj_data.site_xpos[site_id].copy(),
        "position_pinocchio": data.oMf[frame_id].translation.copy(),
        "mujoco_velocity": mj_v,
        "pinocchio_world_velocity": angular_first(
            pin.getFrameVelocity(model, data, frame_id, world)
        ),
        "pinocchio_lwa_velocity": angular_first(
            pin.getFrameVelocity(model, data, frame_id, lwa)
        ),
        "mujoco_acceleration": mj_a,
        "pinocchio_world_spatial_acceleration": angular_first(
            pin.getFrameAcceleration(model, data, frame_id, world)
        ),
        "pinocchio_lwa_spatial_acceleration": angular_first(
            pin.getFrameAcceleration(model, data, frame_id, lwa)
        ),
        "pinocchio_lwa_classical_acceleration": angular_first(
            pin.getFrameClassicalAcceleration(model, data, frame_id, lwa)
        ),
    }


def verify(models):
    """Check against circular kinematics and differences of actual API outputs."""
    errors = {}

    def check(name, actual, expected, atol=1e-11):
        errors[name] = max(
            errors.get(name, 0.0), float(np.max(np.abs(actual - expected)))
        )
        np.testing.assert_allclose(actual, expected, rtol=0, atol=atol, err_msg=name)

    # Nonzero angular acceleration also checks cases beyond the zero-spatial-
    # acceleration hook. Negative speed checks the cross-product signs.
    states = [
        (q, w, alpha)
        for q in np.linspace(0, 2 * np.pi, 13)
        for w, alpha in [(1.0, 0.0), (-0.7, 0.4)]
    ]
    h = 1e-5
    for q, w, alpha in states:
        s = sample(models, q, w, alpha)
        p = np.array([np.cos(q), np.sin(q), 0.0])
        omega, angular_a = np.array([0.0, 0.0, w]), np.array([0.0, 0.0, alpha])
        point_v = np.cross(omega, p)
        point_a = np.cross(angular_a, p) + np.cross(omega, point_v)
        check("position_mujoco", s["position_mujoco"], p)
        check("position_pinocchio", s["position_pinocchio"], p)
        check("velocity_analytic", s["mujoco_velocity"], np.r_[omega, point_v])
        check("velocity_libraries", s["mujoco_velocity"], s["pinocchio_lwa_velocity"])
        check("world_velocity", s["pinocchio_world_velocity"], np.r_[omega, np.zeros(3)])
        check("acceleration_analytic", s["mujoco_acceleration"], np.r_[angular_a, point_a])
        check("acceleration_libraries", s["mujoco_acceleration"],
              s["pinocchio_lwa_classical_acceleration"])
        check("world_spatial_acceleration", s["pinocchio_world_spatial_acceleration"],
              np.r_[angular_a, np.zeros(3)])
        check("lwa_spatial_acceleration", s["pinocchio_lwa_spatial_acceleration"],
              np.r_[angular_a, np.cross(angular_a, p)])
        check("classical_minus_spatial",
              s["pinocchio_lwa_classical_acceleration"] -
              s["pinocchio_lwa_spatial_acceleration"],
              np.r_[np.zeros(3), np.cross(omega, point_v)])

        # Sample a smooth local trajectory with the prescribed acceleration.
        plus = sample(models, q + w*h + 0.5*alpha*h*h, w + alpha*h, alpha)
        minus = sample(models, q - w*h + 0.5*alpha*h*h, w - alpha*h, alpha)
        for key in ("mujoco_velocity", "pinocchio_lwa_velocity"):
            check("finite_difference_" + key, (plus[key] - minus[key]) / (2*h),
                  s["pinocchio_lwa_classical_acceleration"], atol=2e-9)
        check("finite_difference_world",
              (plus["pinocchio_world_velocity"] - minus["pinocchio_world_velocity"]) / (2*h),
              s["pinocchio_world_spatial_acceleration"], atol=2e-9)
    return {"states_checked": len(states), "max_absolute_errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Save the verified results as JSON.")
    args = parser.parse_args()
    models = make_models()
    checks = verify(models)
    at_zero = sample(models, 0.0)
    at_quarter_turn = sample(models, np.pi / 2)
    print(f"MuJoCo {mujoco.__version__}; Pinocchio {pin.__version__}")
    print("r = 1 m, omega = 1 rad/s, angular acceleration = 0")
    print("q = 0: P = (1, 0, 0); vectors are [angular; linear]\n")
    for name, value in at_zero.items():
        clean = np.where(np.abs(value) < 1e-12, 0.0, value)
        print(f"{name:42s} {np.array2string(clean, precision=4, suppress_small=True)}")
    print(f"\nVerified {checks['states_checked']} states; maximum finite-difference error: "
          f"{max(v for k, v in checks['max_absolute_errors'].items() if k.startswith('finite')):.3g}")
    if args.output:
        result = {
            "versions": {"python": platform.python_version(), "numpy": np.__version__,
                         "mujoco": mujoco.__version__, "pinocchio": pin.__version__},
            "conditions": {"radius_m": 1, "speed_rad_s": 1,
                           "angular_acceleration_rad_s2": 0,
                           "six_vector_order": "angular, linear", "gravity": "disabled"},
            "q_0": {k: v.tolist() for k, v in at_zero.items()},
            "q_pi_over_2": {k: v.tolist() for k, v in at_quarter_turn.items()},
            "verification": checks,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
