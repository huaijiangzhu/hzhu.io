# Spatial Acceleration: Notes for a Follow-up

Unpublished material from the original combined draft. The current article ends at LWA velocity. These notes use the rotating-body setup and velocity definitions from that article.


With the velocity comparison fixed, it is tempting to use the same convention for acceleration.

```python
# Populate the acceleration buffers in this sensor-free model.
mujoco.mj_rnePostConstraint(mj_model, mj_data)
acceleration = np.zeros(6)
mujoco.mj_objectAcceleration(
    mj_model, mj_data, mujoco.mjtObj.mjOBJ_SITE,
    site_id, acceleration, 0,
)
print(acceleration[3:])
# [-1.  0.  0.]

a_lwa = pin.getFrameAcceleration(model, data, frame_id, LWA)
print(a_lwa.linear)
# [0. 0. 0.]
```

The angular acceleration is zero in both cases. The linear parts disagree again.

MuJoCo's result is the familiar centripetal acceleration. The point $P$ moves on a circle, so at the instant shown above its acceleration is

$$
\ddot p=\begin{bmatrix}-1\\0\\0\end{bmatrix}\,\mathrm{m/s^2}.
$$

We would also get this by differentiating the LWA velocity:

$$
\frac{dV^{\mathrm{LWA}}}{dt}
=
\begin{bmatrix}
\dot\omega\\
\ddot p
\end{bmatrix}.
$$

Why doesn't `getFrameAcceleration` return that?

In Featherstone's convention, spatial acceleration is the time derivative of spatial velocity. With the world frame fixed and inertial, we can take this derivative component by component:

$$
A^W
=
\frac{dV^W}{dt}.
$$

For our example,

$$
V^W=\begin{bmatrix}\omega\\0\end{bmatrix}
$$

is constant. Therefore $A^W=0$.

Zero remains zero when expressed in another basis. So the same spatial acceleration expressed in LWA must also be zero.

The nonzero derivative of $V^{\mathrm{LWA}}$ cannot be just another coordinate expression of $A^W$. Something changed when we differentiated.

## A Constant Field Can Still Accelerate a Point

Look at the same rotation at two different times.

![Two snapshots of the rotating body. The gray velocity arrows at fixed locations are identical. The material point P has moved, and both its tangential velocity and inward acceleration have changed direction.](/images/featherstone/velocity-field-snapshots.svg)

First look at the square $Q$, which marks a fixed location in space. Different material points pass through it, but their velocities at that location are always the same.

Then follow the blue point $P$. It is the same material point in both pictures, but it has moved to a location with a different velocity.

The field has not changed. The velocity along the point's trajectory has.

To distinguish those two changes, we now need notation that keeps position and time separate. Let $u(x,t)$ mean the velocity assigned to location $x$ at time $t$. Call the field's value at the world origin $v_0(t)=\dot p-\omega\times p$. Our earlier formula then reads

$$
u(x,t)=\omega(t)\times x+v_0(t).
$$

Holding $x$ fixed and differentiating with respect to time gives

$$
\left.\frac{\partial u}{\partial t}\right|_x
=
\dot\omega\times x+\dot v_0.
$$

This is another field of the same form, with coefficients $\dot\omega$ and $\dot v_0$. Those are the components of spatial acceleration in WORLD.

Following $P$ requires the chain rule:

$$
\frac{d}{dt}u(p(t),t)
=
\frac{\partial u}{\partial t}(p(t),t)
+
(\dot p\cdot\nabla)u(p(t),t).
$$

Since $u(x,t)=\omega\times x+v_0$, its spatial variation gives

$$
(\dot p\cdot\nabla)u
=
\omega\times\dot p.
$$

And since $u(p(t),t)=\dot p$, we obtain

$$
\ddot p
=
\frac{\partial u}{\partial t}(p(t),t)
+
\omega\times\dot p.
$$

The left-hand side is the ordinary acceleration of the point. It is the material derivative of the velocity field along that point's trajectory.

The first term on the right is the linear component of spatial acceleration expressed at $P$, with world-aligned axes. Therefore,

$$
A^{\mathrm{LWA}}
=
\begin{bmatrix}
\dot\omega\\
\ddot p-\omega\times\dot p
\end{bmatrix}.
$$

For constant rotation about the world origin, the field derivative is zero. The point's entire acceleration comes from the second term:

$$
\ddot p
=
\omega\times\dot p
=
\omega\times(\omega\times p).
$$

That is the centripetal acceleration. It was never missing; it comes from following a point through the field.

## The Moving Origin Matters

There is a coordinate subtlety here. The LWA axes do not rotate, which makes it easy to think that differentiating its six components needs no correction.

But its origin moves. The linear component of a twist depends on that origin, even when the coordinate axes stay parallel.

In this case the difference is

$$
\frac{dV^{\mathrm{LWA}}}{dt}
=
A^{\mathrm{LWA}}
+
\begin{bmatrix}
0\\
\omega\times\dot p
\end{bmatrix}.
$$

The left-hand side is the six-dimensional combination usually called *classical acceleration*: angular acceleration together with the acceleration of the selected material point. Featherstone derives this particular moving-origin case in [Section VII of *Plücker Basis Vectors*](https://royfeatherstone.org/papers/icra06plucker.pdf).

<div class="remark">
<p class="remark-label">Remark</p>
<p>The same distinction follows from the product rule. If a time-dependent coordinate transformation gives $V^F=\mathcal T(t)V^W$, then</p>
$$
\frac{dV^F}{dt}
=
\mathcal T A^W+\dot{\mathcal T}V^W,
\qquad
A^F=\mathcal T A^W.
$$
<p>Differentiating the coordinates introduces a term from the changing expression frame. That term can vanish in particular cases; a moving frame does not automatically imply a nonzero correction.</p>
</div>

## Back to the Code

Pinocchio provides the classical quantity separately:

```python
a_classical = pin.getFrameClassicalAcceleration(
    model, data, frame_id, LWA
)
print(a_classical.linear)
# [-1.  0.  0.]

np.testing.assert_allclose(
    a_classical.linear,
    a_lwa.linear + np.cross(v_lwa.angular, v_lwa.linear),
)
```

This agrees with MuJoCo's object acceleration for our gravity-free example.

We can also check which acceleration is obtained by finite-differencing the velocity. The supplied example has a `sample` function that evaluates both libraries at a given joint angle, with unit angular speed by default. Along our trajectory, $q(t)=t$, so:

```python
models = make_models()
h = 1e-5
v_plus = sample(models, h)["pinocchio_lwa_velocity"]
v_minus = sample(models, -h)["pinocchio_lwa_velocity"]

dv_dt = (v_plus - v_minus) / (2 * h)
print(dv_dt[3:])
# [-1.  0.  0.]  up to finite-difference error
```

Here `sample` returns all six-vectors in angular-first order. The result agrees with classical acceleration. Differencing the WORLD velocity instead gives zero, agreeing with spatial acceleration in WORLD.

The same behavior holds throughout a full revolution:

![API outputs through one revolution. MuJoCo's linear velocity agrees with Pinocchio LWA, while its linear acceleration agrees with Pinocchio classical LWA. Pinocchio WORLD linear velocity and spatial LWA acceleration are zero in this example.](/images/featherstone/mujoco-pinocchio-comparison.svg)

The [runnable example](/downloads/featherstone-example.zip) was tested with MuJoCo 3.14.0 and Pinocchio 4.1.0. It checks 26 states, including nonzero angular acceleration, against analytic kinematics and finite differences of the actual API outputs.

The setup deliberately queries the same point in both libraries, disables gravity, and avoids time integration. It also accounts for the libraries' different six-vector storage orders. These details keep the comparison focused on the meaning of the quantities.

## Takeaway

A spatial twist specifies a rigid-body velocity field. Its linear component is the field evaluated at the chosen reference origin.

Spatial acceleration describes how that field changes at fixed spatial positions. Classical acceleration follows a material point, whose velocity can change even when the field stays constant.

LWA gives us the familiar point velocity $\dot p$ in world axes. Differentiating it follows the moving point, which is why it gives $\ddot p$ rather than the linear component of Featherstone's spatial acceleration.
