# Exercise 2.2 — Transition Matrix from Conditional Expectations

This exercise studies how to recover a Markov transition matrix from conditional expectations of functions of the state.

The problem is based on Chapter 2 of:

> Lars Ljungqvist and Thomas J. Sargent,\
> *Recursive Macroeconomic Theory*, 4th ed., MIT Press, 2018.

## Problem

Consider a two-state Markov chain and a random variable

$$
y_t = \bar y^\top x_t,
$$

with state values

$$
\bar y =
\begin{pmatrix}
1 \\
5
\end{pmatrix}.
$$

The conditional moments are

$$
E(y_{t+1}\mid x_t)
=
\begin{pmatrix}
1.8 \\
3.4
\end{pmatrix},
$$

and

$$
E(y_{t+1}^2\mid x_t)
=
\begin{pmatrix}
5.8 \\
15.4
\end{pmatrix}.
$$

The goal is to recover a transition matrix consistent with these restrictions and determine whether it is uniquely identified.

## Main result

Using

$$
E(y_{t+1}\mid x_t)=P\bar y
$$

together with the row-sum restrictions on a stochastic matrix gives

$$
P=
\begin{pmatrix}
0.8 & 0.2 \\
0.4 & 0.6
\end{pmatrix}.
$$

The second conditional moment is then used as a consistency check.

## Main idea

The exercise illustrates the inverse problem

$$
\text{conditional expectations}
\longrightarrow
\text{transition probabilities}.
$$

For each current state, the unknown transition probabilities must satisfy both:

$$
\sum_j p_{ij}=1
$$

and

$$
\sum_j p_{ij} y_j
=
E(y_{t+1}\mid x_t=e_i).
$$

Because the two state values are distinct, these restrictions uniquely determine each row of the transition matrix.

## Extension: noisy empirical moments

The Python solution also considers a simple two-state business-cycle model in which quarterly GDP growth can take two representative values:

-   recession: $-2\%$
-   expansion: $3\%$

In an empirical application, conditional moments are estimated from finite samples and may not satisfy the theoretical restrictions of the Markov model exactly.

The extension therefore estimates the transition matrix by minimum distance, choosing the transition probabilities that best match both the estimated conditional first and second moments.

This turns the exact identification problem into an econometric estimation problem:

$$
\text{noisy sample moments}
\longrightarrow
\hat P.
$$

## Files

-   `solution.tex` — analytical solution and business-cycle extension
-   `solution.pdf` — compiled version of the solution
-   `solution.py` — Python implementation of the transition-matrix recovery and minimum-distance extension

## Related topics

-   finite-state Markov chains
-   conditional expectations
-   transition probabilities
-   identification
-   minimum-distance estimation
-   business-cycle regime models
