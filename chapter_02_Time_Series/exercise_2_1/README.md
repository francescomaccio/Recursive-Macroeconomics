# Exercise 2.1 — Likelihood of Markov-Chain Histories

This folder contains the analytical and computational solution to Exercise 2.1 from 
*Recursive Macroeconomic Theory* by Lars Ljungqvist and Thomas J. Sargent.

## Description

The exercise considers a two-state Markov chain characterized by the transition matrix

\[
P =
\begin{pmatrix}
0.9 & 0.1 \\
0.3 & 0.7
\end{pmatrix}
\]

and the initial probability distribution

\[
\pi_0 =
\begin{pmatrix}
0.5 \\
0.5
\end{pmatrix}.
\]

The state of the Markov chain determines the observed random variable \(y_t\) through

\[
y_t = \bar y x_t,
\]

with the two possible observed values

\[
\bar y =
\begin{pmatrix}
1 \\
5
\end{pmatrix}.
\]

The objective is to compute the likelihood of three different observed histories over five periods:

- \(1,5,1,5,1\)
- \(1,1,1,1,1\)
- \(5,5,5,5,5\)

The exercise provides a simple introduction to the likelihood of finite-state Markov processes and illustrates
how persistence and transition probabilities determine the probability of observing a particular time-series history.

---

## Contents

The exercise is solved both analytically and computationally.

- `solution.tex` — complete analytical derivation written in LaTeX
- `solution.pdf` — compiled version of the analytical solution
- `solution.py` — Python implementation of the likelihood calculations

The Python implementation is written in a general form so that the likelihood of an arbitrary observed history can be evaluated rather than hard-coding only the three paths considered in the exercise.

---

## Main Idea

For a Markov chain with state history

\[
x_0,x_1,\ldots,x_T,
\]

the joint probability of observing the complete path is

\[
\Pr(x_0,x_1,\ldots,x_T)
=
\pi_0(x_0)
\prod_{t=0}^{T-1}
P_{x_t,x_{t+1}}.
\]

Therefore, computing the likelihood of a history requires two components:

1. the probability of the initial state, given by \(\pi_0\);
2. the product of all transition probabilities associated with the observed path.

Since the values of \(y_t\) uniquely identify the underlying state in this exercise,

\[
y_t=1 \Longleftrightarrow x_t=1,
\qquad
y_t=5 \Longleftrightarrow x_t=2,
\]

each observed history can first be translated into its corresponding sequence of Markov states.

For example,

\[
(1,5,1,5,1)
\]

corresponds to the state path

\[
(1,2,1,2,1),
\]

whose likelihood is

\[
\pi_0(1)
P_{12}
P_{21}
P_{12}
P_{21}.
\]

The exercise also highlights the economic and statistical meaning of **state persistence**. Since

\[
P_{11}=0.9
\]

is larger than

\[
P_{22}=0.7,
\]

the first state is more persistent than the second. Histories involving repeated switching between states are considerably less likely because some of the required transitions have relatively low probabilities.

---

## Computational Extensions

In addition to reproducing the analytical solution, the Python implementation extends the exercise in several directions.

### 1. General path-likelihood function

A reusable function is implemented to evaluate

\[
L(x_0,\ldots,x_T)
=
\pi_0(x_0)
\prod_{t=0}^{T-1}P_{x_t,x_{t+1}}
\]

for any admissible sequence of observations.

This separates the economic model from the particular histories used in the textbook exercise.

### 2. Log-likelihood

For long histories, multiplying many probabilities can lead to numerical underflow.

The likelihood can instead be evaluated through the log-likelihood

\[
\log L
=
\log \pi_0(x_0)
+
\sum_{t=0}^{T-1}
\log P_{x_t,x_{t+1}}.
\]

The implementation verifies numerically that

\[
L = \exp(\log L).
\]

This provides a first connection between Markov-chain probabilities and likelihood-based
estimation methods used later in econometrics.

### 3. Analytical versus numerical verification

The results obtained by the general Python function are compared with the probabilities derived analytically.

Automated numerical checks are used to verify that the two approaches coincide.

### 4. Monte Carlo simulation

As an additional experiment, repeated histories can be simulated from the Markov chain.

The simulations can be used to study how the transition matrix determines the empirical frequency of different state paths
and to illustrate the persistence of the two states.

This provides a computational link between

\[
\text{transition probabilities}
\rightarrow
\text{simulated histories}
\rightarrow
\text{empirical frequencies}.
\]

---

## Concepts Covered

- Finite-state Markov chains
- Transition matrices
- State persistence
- Conditional probabilities
- Joint path probabilities
- Likelihood functions
- Log-likelihood functions
- Numerical verification
- Monte Carlo simulation

---

## Reference

Ljungqvist, L. and Sargent, T. J., *Recursive Macroeconomic Theory*, 4th ed., MIT Press, 2018, Exercise 2.1.

> This repository contains my own analytical derivations, explanations, and computational implementations. 
The original textbook exercise is referenced rather than reproduced in full.
