# Featherstone: a runnable MuJoCo / Pinocchio example

A single hinge rotates around the world z-axis. An attached frame P is one metre
from the axis. Both libraries evaluate the same joint position, velocity and
acceleration. There is no viewer, contact, gravity, or simulation time-stepping.

This compares **API conventions**: MuJoCo uses spatial vectors internally,
and Pinocchio provides both spatial and classical acceleration interfaces.

The current blog post covers velocity and ends with LOCAL_WORLD_ALIGNED. The
acceleration experiments below are retained as material for a possible
follow-up; they are not part of the current article.

## Run

Tested with Python 3.12.14, MuJoCo 3.14.0, Pinocchio 4.1.0 and NumPy 2.5.3 on macOS
arm64. The robotics library's PyPI package is `pin`, imported as `pinocchio`.

From this directory:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python compare_libraries.py --output verified-results.json
.venv/bin/python plot_figures.py
```

The plot script writes SVG and PNG versions to `static/images/featherstone/`
and packages the source into `static/downloads/featherstone-example.zip`.
The archive preserves the `examples/featherstone/`
directory structure, so these commands also work after extracting it.
`compare_libraries.py` checks 26 states against circular-motion formulas, compares
the libraries, and finite-differences their actual velocity outputs. Additional
states include negative angular velocity and nonzero angular acceleration.

## The two surprises

At q = 0, P = (1, 0, 0) m, with angular velocity (0, 0, 1) rad/s and zero angular
acceleration:

| Query | Linear velocity (m/s) |
| --- | --- |
| MuJoCo `mj_objectVelocity(..., flg_local=0)` | (0, 1, 0) |
| Pinocchio `getFrameVelocity(..., WORLD)` | (0, 0, 0) |
| Pinocchio `getFrameVelocity(..., LOCAL_WORLD_ALIGNED)` | (0, 1, 0) |

All three angular velocities are (0, 0, 1). WORLD's linear part is the rigid-body
velocity field evaluated at the world origin; LWA's linear part is the velocity
of P, expressed on world axes.

Changing to LWA fixes the velocity comparison. Applying the same change to the
acceleration comparison still leaves a mismatch:

| Query | Linear acceleration (m/s²) |
| --- | --- |
| MuJoCo `mj_objectAcceleration(..., flg_local=0)` | (-1, 0, 0) |
| Pinocchio `getFrameAcceleration(..., LOCAL_WORLD_ALIGNED)` | (0, 0, 0) |
| Pinocchio `getFrameClassicalAcceleration(..., LOCAL_WORLD_ALIGNED)` | (-1, 0, 0) |

All angular accelerations are zero. In this example the time derivative of the
rigid-body velocity field is zero. The material point P still has centripetal
acceleration, which is what the classical interface returns.

The central difference of LWA velocity agrees with classical acceleration.
The central difference of WORLD velocity agrees with spatial acceleration
expressed in WORLD. See `verified-results.json` for the measured errors.

## Figures

The current article uses `body-displacement` to show the arrows p, x, and r,
and `twist-chain` for the two-link composition example. It then assigns numerical
values to the first setup for the API comparison. Both figures have SVG and PNG
versions.
SVG glyphs are embedded as paths to preserve mathematical accents and spacing
when a reader does not have the plotting font installed.
Mathematical labels use Computer Modern through Matplotlib MathText, with upright
units and italic variables; prose labels use a matching serif style.

The separate `rotating-frame` illustration, velocity-field snapshots, and full
API comparison plot are retained for the accompanying experiments. The plot
script regenerates all figures.

## Reproduction details

- Query a MuJoCo **site** and the matching Pinocchio operational frame, so both
  queries use the same point. A body origin need not coincide with its centre of mass.
- `flg_local=0` selects world **orientation**; it does not move the query origin
  to the world origin.
- MuJoCo's object functions return `[angular; linear]`. Pinocchio's raw `.vector`
  stores `[linear; angular]`; the script uses `.angular` and `.linear` to normalize
  the printed ordering.
- Call `mj_rnePostConstraint` before querying acceleration in this sensor-free
  model, so that MuJoCo's acceleration buffers are populated.
- Gravity is disabled to isolate the kinematic distinction.
- `mj_inverse` accepts the prescribed `qacc`; the comparison does not depend on
  an integration scheme or a dynamics controller.
- MuJoCo's internal `cvel` / `cacc` use a different reference-point convention
  and are not substitutes for the object query functions used here.

## References

- [MuJoCo object velocity and acceleration API](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-objectvelocity)
- [MuJoCo coordinate conventions](https://mujoco.readthedocs.io/en/stable/programming/simulation.html#coordinate-frames-and-transformations)
- [MuJoCo object-query implementation](https://github.com/google-deepmind/mujoco/blob/main/src/engine/engine_core_util.c)
- [Pinocchio reference-frame conventions](https://gepettoweb.laas.fr/doc/stack-of-tasks/pinocchio/devel/doxygen-html/group__pinocchio__multibody.html)
- [Pinocchio frame interfaces](https://gepettoweb.laas.fr/doc/stack-of-tasks/pinocchio/jnrh2023/template/frame.html)
- [Featherstone, Plücker Basis Vectors, section VII](https://royfeatherstone.org/papers/icra06plucker.pdf)
