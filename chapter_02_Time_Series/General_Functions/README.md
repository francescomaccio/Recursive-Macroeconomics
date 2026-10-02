# General Functions — Chapter 2: Time Series

This folder contains a collection of reusable Python functions for the main computational tools introduced in **Chapter 2 — Time Series** of *Recursive Macroeconomic Theory* by Lars Ljungqvist and Thomas J. Sargent.

Unlike the exercise-specific folders in this repository, the purpose of this section is not to solve a particular exercise. Instead, it develops a small library of **general-purpose functions** that can be reused across different exercises and macroeconomic applications.

The general approach followed in each notebook is:

1. introduce the relevant mathematical framework;
2. define reusable Python functions implementing the main operations;
3. explain the inputs and outputs of each function;
4. verify the relevant mathematical properties;
5. construct a detailed economic application;
6. use simulations and visualizations to provide intuition for the underlying dynamics.

The objective is therefore to connect

\[
\boxed{
\text{economic theory}
\longrightarrow
\text{mathematical representation}
\longrightarrow
\text{Python implementation}
\longrightarrow
\text{economic interpretation}
}
\]

rather than treating the code as a collection of isolated numerical routines.

---

## Relation to Chapter 2

Chapter 2 introduces two fundamental ways of representing stochastic dynamics:

- **finite-state Markov chains**;
- **stochastic linear difference equations**.

It then develops tools for studying forecasting, stationary distributions, moments, impulse responses, prediction, discounting, estimation, and filtering.

These objects provide many of the computational building blocks used throughout recursive macroeconomics. In particular, Chapter 2 develops Markov chains, continuous-state processes, stochastic linear difference equations, first and second moments, impulse response functions, prediction and discounting, and the Kalman filter.

The notebooks in this folder translate these theoretical objects into general Python functions that can subsequently be applied to different economic environments.

---

## Folder Structure

The intended structure is:

```text
general_functions/
│
├── README.md
│
├── markov_chains.ipynb
├── linear_state_space.ipynb
├── kalman_filter.ipynb
└── ...
