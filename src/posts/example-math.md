---
title: "Testing LaTeX Math Rendering"
date: "2024-01-01"
description: "An example post demonstrating LaTeX math support in the blog"
slug: "example-math"
---

This post demonstrates the math rendering capabilities of the blog using KaTeX.

## Inline Math

The famous mass-energy equivalence formula $E = mc^2$ shows the relationship between energy and mass. We can also write inline expressions like $\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$.

## Display Math

The Cauchy-Schwarz inequality:

$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$

Euler's identity, often considered one of the most beautiful equations:

$$e^{i\pi} + 1 = 0$$

The definition of the Gaussian distribution:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$

## Matrices and Vectors

A simple rotation matrix in 2D:

$$R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$

## Physics Equations

Newton's second law of motion:

$$\mathbf{F} = m\mathbf{a}$$

The Schrodinger equation:

$$i\hbar\frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat{H}\Psi(\mathbf{r},t)$$

## Code Example

Here's a simple Python function:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

This demonstrates that code blocks work alongside math rendering.
