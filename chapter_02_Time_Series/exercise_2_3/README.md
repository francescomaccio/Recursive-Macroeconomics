# Exercise 2.3 — Markov Consumption Processes and Bayesian Model Comparison

This exercise studies how alternative Markov processes for consumption can generate the same unconditional distribution while implying very different dynamic behavior.

The exercise combines three main ideas from Chapter 2 of *Recursive Macroeconomic Theory* by Lars Ljungqvist and Thomas J. Sargent:

-   discounted expected utility under Markov consumption risk;
-   likelihood-based comparison of competing Markov models;
-   Bayesian updating over alternative data-generating processes.

The solution also develops several computational extensions that give the exercise a more explicit macroeconomic interpretation.

## Files

-   `solution.pdf` — complete written solution, including the analytical derivation, numerical results, economic interpretation, and computational extensions;
-   `solution.tex` — LaTeX source of the written solution;
-   `solution.py` — Python implementation of the numerical solution and extensions.

## Main Setup

Consumption is governed by a finite-state Markov chain with transition matrix $P$ and initial distribution $\pi_0$.

The consumer has CRRA utility

$$
u(c)=\frac{c^{1-\gamma}}{1-\gamma},
$$

and ranks stochastic consumption processes according to

$$
E\sum_{t=0}^{\infty}\beta^t u(c_t).
$$

For each initial state, the conditional discounted value satisfies

$$
v=(I-\beta P)^{-1}u,
$$

while the ex ante value is

$$
V=\pi_0'v.
$$

The exercise compares two two-state consumption processes:

$$
P_1=
\begin{pmatrix}
1 & 0\\
0 & 1
\end{pmatrix},
\qquad
P_2=
\begin{pmatrix}
0.5 & 0.5\\
0.5 & 0.5
\end{pmatrix},
$$

with common initial distribution

$$
\pi_0=
\begin{pmatrix}
0.5\\
0.5
\end{pmatrix},
$$

and consumption values

$$
\bar c=
\begin{pmatrix}
1\\
5
\end{pmatrix}.
$$

Process 1 is perfectly persistent: the initial state is absorbing. Process 2 is serially independent: each period the next state is drawn with equal probability from the two possible states. :

## Computational Solution

The Python implementation reproduces the main results of the exercise.

For $\beta=0.95$ and $\gamma=2.5$,

$$
V_1=V_2=-7.262951.
$$

For $\gamma=4$,

$$
V_1=V_2=-3.360000.
$$

Hence, the consumer is ex ante indifferent between the two processes in both cases. The reason is that both models generate the same unconditional distribution of consumption at every date, even though they have very different persistence properties.

The conditional value vectors, however, differ substantially across the two models because the initial state has very different implications for future consumption.

## Likelihood and Bayesian Model Comparison

The exercise then considers an econometrician who observes consumption histories but does not know which of the two Markov processes generated the data.

For the sample

$$
1,1,1,1,1,1,1,1,1,1,
$$

the likelihoods are

$$
\Pr(\text{data}\mid M_1)=0.5,
$$

and

$$
\Pr(\text{data}\mid M_2)=0.0009765625.
$$

With equal prior probabilities, the posterior probabilities become approximately

$$
\Pr(M_1\mid\text{data})=0.998051,
$$

and

$$
\Pr(M_2\mid\text{data})=0.001949.
$$

Thus, a long sequence of identical observations provides strong evidence in favor of the persistent process. :chatgpt-content-reference{index="3"}

For the second sample,

$$
1,5,5,1,5,5,1,5,1,5,
$$

Process 1 assigns zero probability to the data because it does not allow transitions between states. Therefore,

$$
\Pr(M_1\mid\text{data})=0,
\qquad
\Pr(M_2\mid\text{data})=1.
$$

This illustrates the difference between an event that is merely unlikely under a model and one that is impossible under that model.

## Extensions

The Python solution adds several extensions that deepen the economic interpretation of the exercise.

### Sequential Bayesian Learning

Posterior model probabilities are updated after each new observation rather than only at the end of the sample.

This shows how evidence accumulates gradually over time and provides a natural interpretation for real-time macroeconomic inference. A long sequence of low-consumption observations increasingly favors a persistent-shock model.

### Persistence and Autocorrelation

The theoretical autocorrelation function of consumption differs sharply across the two models.

For Process 1,

$$
\operatorname{Corr}(c_t,c_{t+k})=1
$$

for every positive lag.

For Process 2,

$$
\operatorname{Corr}(c_t,c_{t+k})=0.
$$

This provides a simple interpretation in terms of permanent versus transitory income shocks.

### Expected Duration of Consumption States

The expected duration of a Markov state is

$$
E[D_i]=\frac{1}{1-P_{ii}}.
$$

Under Process 1, both states are absorbing, so expected duration is infinite.

Under Process 2, the expected duration of either state is two periods.

This gives an intuitive measure of persistence and connects naturally to models of unemployment spells, income risk, and consumption smoothing.

### Certainty-Equivalent Consumption

The solution also converts lifetime utility into a more interpretable welfare measure.

For $\gamma=2.5$,

$$
c^{CE}=1.499283,
$$

while for $\gamma=4$,

$$
c^{CE}=1.256579.
$$

The decline in the certainty equivalent as $\gamma$ rises reflects the greater sensitivity of a more risk-averse consumer to low-consumption outcomes.

## Economic Interpretation

The central lesson of the exercise is that

$$
\text{same unconditional distribution}
\neq
\text{same stochastic process}.
$$

The two models generate the same one-period distribution of consumption, but radically different time-series dependence.

This distinction matters because the transition matrix determines:

-   conditional lifetime values from the consumer's perspective;
-   persistence and expected duration of shocks;
-   likelihoods of observed histories;
-   posterior beliefs over competing models.

The exercise therefore connects welfare analysis, time-series dynamics, likelihood methods, and Bayesian learning in a simple finite-state setting. 

## Reference

Ljungqvist, L. and Sargent, T. J. (2018).\
*Recursive Macroeconomic Theory*, 4th edition. MIT Press.
