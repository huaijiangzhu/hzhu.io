---
title: "Finite Difference on Finite Difference"
date: "2026-09-05"
description: "Does finite differencing a finite difference amplify the error by the inverse of the step size? Not necessarily."
slug: "finite-difference-on-finite-difference"
---
I was recently writing a finite-difference test for an analytic acceleration implementation.

Suppose we have a smooth trajectory $x(t)$, and the implementation gives its acceleration $a(t)=x''(t)$. To test it independently, we can estimate velocity with a central difference,

$$
\hat v(t)
=
\frac{x(t+h_v)-x(t-h_v)}{2h_v},
$$

and then finite-difference that estimate again:

$$
\hat a(t)
=
\frac{\hat v(t+h_a)-\hat v(t-h_a)}{2h_a}.
$$

The question is how much numerical error to expect in $\hat a(t)$. That determines the finite-difference step sizes and, in turn, the test tolerance.

## One Central Difference

For a smooth function $f(t)$,

$$
\frac{f(t+h)-f(t-h)}{2h}
=
f'(t)
+
\frac{h^2}{6}f^{(3)}(t)
+
O(h^4).
$$

So the truncation error is $O(h^2)$.

Floating-point arithmetic adds another source of error. If we ignore scale factors and other constants, the subtraction $f(t+h)-f(t-h)$ carries $O(\epsilon)$ roundoff, where $\epsilon$ is machine epsilon. Dividing by $h$ turns this into $O(\epsilon/h)$.

A simple error model is therefore

$$
E(h)
=
C_t h^2
+
C_r\frac{\epsilon}{h},
$$

where $C_t$ and $C_r$ collect the truncation and roundoff constants.

The optimal step minimizes $E(h)$. Setting $dE/dh=0$ gives

$$
h_{\mathrm{opt}}
=
\left(
\frac{C_r}{2C_t}\epsilon
\right)^{1/3},
$$

so, up to constants,

$$
h_{\mathrm{opt}}\sim\epsilon^{1/3}.
$$

The ratio $C_r/C_t$ only enters through a cube root, so the optimal step is not very sensitive to moderate errors in these constants. For order-of-magnitude reasoning, treating them as order one is usually enough.

## A Naive Nested Error Model

The velocity estimate has error

$$
\hat v(t)-v(t)
=
O(h_v^2)
+
O\left(\frac{\epsilon}{h_v}\right).
$$

The acceleration estimate applies another central difference and divides by $h_a$. If we treat both parts of the inner error as independent perturbations at each time sample, we would get

$$
E_a
\stackrel{?}{=}
O(h_a^2)
+
O\left(\frac{h_v^2}{h_a}\right)
+
O\left(\frac{\epsilon}{h_vh_a}\right).
$$

The problem with this model is that the inner truncation error is not an independent perturbation at each time sample. It has smooth temporal structure.

## The Inner Truncation Error Is Smooth

The inner central difference has the more specific expansion

$$
\hat v(t)
=
x'(t)
+
\frac{h_v^2}{6}x^{(3)}(t)
+
O(h_v^4).
$$

Its leading truncation error is therefore $\frac{h_v^2}{6}x^{(3)}(t)$, which varies smoothly with $t$.

Substituting this expansion into the outer central difference gives

$$
\hat a(t)
=
x''(t)
+
\frac{h_a^2+h_v^2}{6}x^{(4)}(t)
+
O\left(
h_a^4+h_a^2h_v^2+h_v^4
\right).
$$

<div class="remark">
<p class="remark-label">Remark</p>
<p>The outer difference is applied to $\hat v$ as a function of $t$, which gives</p>
$$
\hat a(t)
=
\hat v'(t)
+
\frac{h_a^2}{6}\hat v^{(3)}(t)
+
O(h_a^4).
$$
<p>Evaluating $\hat v'$ and $\hat v^{(3)}$ uses the fact that the derivative operator and a constant shift operator commute. The central difference is a combination of two such shifts, so</p>
$$
\hat v^{(k)}(t)
=
\frac{x^{(k)}(t+h_v)-x^{(k)}(t-h_v)}{2h_v}.
$$
<p>Each is then a central difference of $x'$ and $x^{(3)}$, giving $\hat v'=x''+\frac{h_v^2}{6}x^{(4)}+O(h_v^4)$ and $\hat v^{(3)}=x^{(4)}+O(h_v^2)$. Substituting recovers the expansion above.</p>
</div>

So the truncation error is

$$
\hat a(t)-a(t)
=
O(h_a^2)+O(h_v^2).
$$

The second finite difference does not turn the inner $O(h_v^2)$ truncation error into $O(h_v^2/h_a)$.

The outer difference does divide by $h_a$, but the change in the inner truncation bias between $t-h_a$ and $t+h_a$ is itself $O(h_a h_v^2)$. The $h_a$ cancels.

Roundoff does not have the same smooth dependence on time. The inner roundoff is $O(\epsilon/h_v)$, and the outer finite difference introduces another factor of $1/h_a$.

The leading error model is therefore

$$
E(h_v,h_a)
=
C_t\left(h_v^2+h_a^2\right)
+
C_r\frac{\epsilon}{h_vh_a}.
$$

## Choosing $h_v$ and $h_a$

We can choose both step sizes by minimizing this error model.

The optimum satisfies

$$
\frac{\partial E}{\partial h_v}
=
2C_t h_v
-
C_r\frac{\epsilon}{h_v^2h_a}
=
0,
$$

and

$$
\frac{\partial E}{\partial h_a}
=
2C_t h_a
-
C_r\frac{\epsilon}{h_vh_a^2}
=
0.
$$

These two equations imply $h_v=h_a$.

So equal inner and outer step sizes are a consequence of this model, not an assumption.

Writing both as $h$,

$$
E(h)
=
2C_t h^2
+
C_r\frac{\epsilon}{h^2}.
$$

Setting $dE/dh=0$ gives

$$
h_{\mathrm{opt}}
=
\left(
\frac{C_r}{2C_t}\epsilon
\right)^{1/4}.
$$

Therefore,

$$
h_v^{\mathrm{opt}}
\sim
h_a^{\mathrm{opt}}
\sim
\epsilon^{1/4}.
$$

For double precision, $\epsilon^{1/4}$ is roughly $10^{-4}$.

The constants matter even less here than in the first-derivative case, since their ratio only enters through a fourth root.

At the optimum, the minimum error scales as

$$
E_{\min}\sim\epsilon^{1/2}.
$$

This gives the expected numerical floor up to the problem-dependent constants that the simple model leaves out.

For a test, a reasonable workflow is to choose $h_v$ and $h_a$ near this scale, sweep around them numerically, observe the actual error floor, and set the tolerance above that floor with some margin.

## Takeaway

The key point is that finite-difference truncation error has temporal structure.

For a smooth trajectory, the leading truncation bias is itself smooth in time. Applying another finite difference therefore differentiates that bias; it does not simply divide its magnitude by the new step size.

That is why the inner $O(h_v^2)$ truncation error remains $O(h_v^2)$, while roundoff picks up the additional $1/h_a$.
