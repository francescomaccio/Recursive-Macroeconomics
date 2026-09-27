"""
Exercise 2.2

Consider a two-state Markov chain. Consider a random variable y_t = y^barx_t where y^bar = [1, 5]. It is known that E(y_{t+1}|x_t)=[1.8, 3.4]
and that E(y_{t+1}^2| x_t) = [5.8, 15.4]. Find a transition matrix consistent with these conditional expectations. Is this transition
matrix unique?    
    
"""

import numpy as np
from scipy.optimize import linprog


def transition_from_expectations(functions, expectations):
    """
    Find a row-stochastic transition matrix P satisfying

        P @ functions = expectations

    together with

        P[i, j] >= 0
        sum_j P[i, j] = 1

    Parameters
    ----------
    functions : array_like
        Matrix whose columns contain functions of the Markov state.

        If there are n states and k functions:
            shape = (n, k)

    expectations : array_like
        Conditional expectations of those functions for each current state.

        shape = (n, k)

    Returns
    -------
    P : ndarray
        A transition matrix consistent with the supplied conditional expectations.
    """

    functions = np.asarray(functions, dtype=float)
    expectations = np.asarray(expectations, dtype=float)

    n = functions.shape[0]

    # Add the constant function 1.
    # This imposes that every row of P sums to 1.
    A = np.column_stack([
        np.ones(n),
        functions
    ])

    # Corresponding expected values:
    # E[1 | x_t] = 1
    B = np.column_stack([
        np.ones(n),
        expectations
    ])

    P = np.empty((n, n))

    # Solve each row of P separately.
    for i in range(n):

        # We want:
        #
        #     p_i @ A = B[i]
        #
        # or equivalently
        #
        #     A.T @ p_i = B[i]

        result = linprog(
            c=np.zeros(n),
            A_eq=A.T,
            b_eq=B[i],
            bounds=[(0, 1)] * n,
            method="highs"
        )

        if not result.success:
            raise ValueError(
                f"No valid transition probabilities exist for state {i}."
            )

        P[i] = result.x

    # Clean very small numerical errors
    P[np.abs(P) < 1e-12] = 0.0

    return P

y = np.array([1, 5])

y_squared = y**2

functions = np.column_stack([
    y,
    y_squared
])

Ey = np.array([1.8, 3.4])
Ey2 = np.array([5.8, 15.4])

expectations = np.column_stack([
    Ey,
    Ey2
])

P = transition_from_expectations(
    functions,
    expectations
)

print(P)

### MINIMUM DISTANCE TRANSITION MATRIX ESTIMATOR EXTENSION ###

def minimum_distance_transition(
    values,
    mean_estimates,
    second_moment_estimates,
    grid_size=10001
):
    """
    Estimate a two-state transition matrix when empirical conditional
    moments do not satisfy the model restrictions exactly.

    The function chooses the transition probability q for each current
    state that minimizes the squared distance between:

        1. empirical and model-implied conditional means
        2. empirical and model-implied conditional second moments

    Parameters
    ----------
    values :
        Values associated with the two states.

    mean_estimates :
        Estimated E[y_{t+1} | x_t = i].

    second_moment_estimates :
        Estimated E[y_{t+1}^2 | x_t = i].

    grid_size :
        Number of possible transition probabilities between 0 and 1
        considered in the search.

    Returns
    -------
    P :
        Estimated 2x2 transition matrix.
    """

    values = np.asarray(values, dtype=float)
    mean_estimates = np.asarray(mean_estimates, dtype=float)
    second_moment_estimates = np.asarray(
        second_moment_estimates,
        dtype=float
    )

    q_grid = np.linspace(0, 1, grid_size)

    P = np.empty((2, 2))

    for i in range(2):

        model_mean = (
            (1 - q_grid) * values[0]
            + q_grid * values[1]
        )

        model_second_moment = (
            (1 - q_grid) * values[0]**2
            + q_grid * values[1]**2
        )

        distance = (
            (model_mean - mean_estimates[i])**2
            +
            (
                model_second_moment
                - second_moment_estimates[i]
            )**2
        )

        best_q = q_grid[np.argmin(distance)]

        P[i] = [
            1 - best_q,
            best_q
        ]

    return P

growth = np.array([-2, 3])

conditional_mean = np.array([
    -0.8,   # current recession
     2.4    # current expansion
])

conditional_second_moment = np.array([
    5.4,
    8.1
])


P_md=minimum_distance_transition(
    growth,
    conditional_mean,
    conditional_second_moment
)

print(P_md)

def forecast_function(P, values, current_states, k):
    """
    This function gives a forecast of the expected future value of a variable when that
    variable depends on the state of a Markov chain.
    P = transition matrix of the Markov chain,
    values = numerical value of y corresponding to each state of the Markov chain,
    current_states = the current state of the Markov chain,
    k = number of steps ahead to forecast.
    """
    Pk = np.linalg.matrix_power(P, k)
    "Calculates the k-th power of the transition matrix P, which gives the transition probabilities after k steps."
    return round((Pk @ values)[current_states], 2)


for state in range(2):

    implied_mean = forecast_function(
        P_md,
        growth,
        state,
        1
    )

    implied_second_moment = forecast_function(
        P_md,
        growth**2,
        state,
        1
    )

    print(
        f"State {state}: "
        f"mean data = {conditional_mean[state]}, "
        f"mean model = {implied_mean}, "
        f"second moment data = {conditional_second_moment[state]}, "
        f"second moment model = {implied_second_moment}"
    )
