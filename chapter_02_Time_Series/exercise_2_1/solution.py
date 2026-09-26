## SOLUTION TO EXERCISE 2.1

import numpy as np

def markov_loglik(path, P, pi0):
    """
    This function computes the log-likelihood of a given path in a Markov chain.
    path = sequence of states observed,
    P = transition matrix of the Markov chain,
    pi0 = initial distribution over states.
    """
    path = np.asarray(path, dtype = int)
    "Converts the input path into a NumPy array of integers."
    
    probs = [pi0[path[0]]]
    
    for t in range(len(path)-1):
        probs.append(
            P[path[t], path[t+1]]
        )
    probs = np.array(probs)
    "Calculates the probabilities of the observed transitions in the path based on the transition matrix P"
    
    if np.any(probs == 0):
        return -np.inf
    "If any of the probabilities are zero, the log-likelihood is negative infinity."
    
    return np.log(probs).sum()
    """
    Returns the sum of the logarithms of the transition probabilities, which is the log-likelihood of the observed path.
    """

path_a = np.array([0, 1, 0, 1, 0])
path_b = np.array([0, 0, 0, 0, 0])
path_c = np.array([1, 1, 1, 1, 1])

P = np.array([[0.9, 0.1], [0.3, 0.7]])
pi0 = np.array([0.5, 0.5])

print("EXERCISE 2.1")
print("=" * 60)

for label, path in [("a", path_a), ("b", path_b), ("c", path_c)]:

    loglik = markov_loglik(path, P, pi0)

    # Recover the likelihood from the log-likelihood.
    likelihood = np.exp(loglik)

    print(f"\nPath {label}: {path}")
    print(f"Log-likelihood : {loglik:.6f}")
    print(f"Likelihood     : {likelihood:.6f}")
    
## EXTENSION I: ANALYTICAL VS COMPUTATIONAL RESULTS

analytical_likelihoods = {
    "a": 0.5 * 0.1 * 0.3 * 0.1 * 0.3,
    "b": 0.5 * (0.9**4),
    "c": 0.5 * (0.7**4),
}


print("\n\nANALYTICAL VS COMPUTATIONAL RESULTS")
print("=" * 60)

for label, path in [("a", path_a), ("b", path_b), ("c", path_c)]:

    computed = np.exp(
        markov_loglik(path, P, pi0)
    )

    analytical = analytical_likelihoods[label]

    print(
        f"Path {label}: "
        f"analytical = {analytical:.6f}, "
        f"computed = {computed:.6f}"
    )

    assert np.isclose(
        analytical,
        computed
    )

print("\nAll analytical and computational results coincide.")

## EXTENSION II: MAPPING OBSERVED VALUES INTO MARKOV STATES


print("\n\nMAPPING OBSERVED VALUES INTO MARKOV STATES")
print("=" * 60)

def map_to_states(observations, y_values):
    """
    Translate observed y_values into zero-indexed Markov states.

    Example
    [1, 5, 1] -> [0, 1, 0]
    """

    mapping = {
        value: state
        for state, value in enumerate(y_values)
    }

    try:
        return np.array(
        [   mapping[value] for value in observations],
            dtype = int
     )

    except KeyError as exc:
        raise ValueError(
            f"Observed value {exc.args[0]} is not associated with any state."
        )

def observed_path_loglik(observations, P, pi0, y_values):
    """
    Compute the log-likelihood of a path of observed values by mapping them into Markov states.
    """
    
    states = map_to_states(
        observations,
        y_values
    )
    
    return markov_loglik(
        states,
        P,
        pi0
    )
    
observed_paths = {
    "a": [1, 5, 1, 5, 1],
    "b": [1, 1, 1, 1, 1],
    "c": [5, 5, 5, 5, 5],
}

print("\n\nLIKELIHOOD OF OBSERVED PATHS")
print("=" * 60)

for label, observations in observed_paths.items():
    
    loglik = observed_path_loglik(
        observations,
        P,
        pi0,
        y_values = [1, 5]
    )
    
    likelihood = np.exp(loglik)
    
    print(
        f"Path {label}: "
        f"{observations} -> "
        f"L = {likelihood:.6f}"
    )    

## MONTE CARLO SIMULATION

def simulate_markov(P, T, s0=None, pi0=None, seed=None):
    """
    Simulate a finite-state Markov chain.

    Parameters
    ----------
    P : array-like
        Transition matrix. P[i, j] gives the probability of moving
        from state i to state j.

    T : int
        Number of time periods to simulate.

    s0 : int, optional
        Initial state. If provided, the simulation starts from this state.

    pi0 : array-like, optional
        Initial probability distribution. Used only if s0 is None.

    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    states : ndarray
        Realized sequence of Markov states over T periods.
    """

    rng = np.random.default_rng(seed)

    P = np.asarray(P, dtype=float)
    n = P.shape[0]

    states = np.empty(T, dtype=int)

    # Initial state
    if s0 is not None:
        states[0] = s0

    elif pi0 is not None:
        states[0] = rng.choice(
            n,
            p=np.asarray(pi0, dtype=float)
        )

    else:
        raise ValueError(
            "Either s0 or pi0 must be provided."
        )

    # Simulate subsequent states
    for t in range(T - 1):
        states[t + 1] = rng.choice(
            n,
            p=P[states[t]]
        )

    return states

simulated_path = simulate_markov(
    P=P,
    T=20,
    pi0=pi0,
    seed=42
)

print("\n\nSIMULATED MARKOV PATH")
print("=" * 60)
print(simulated_path)

## MONTE CARLO CHECK OF THE THEORETICAL LIKELIHOOD


def estimate_path_frequency(
    target_path,
    P,
    pi0,
    n_simulations=100_000,
    seed=42
):
    """
    Estimate the probability of a target Markov path
    using Monte Carlo simulation.
    """

    rng = np.random.default_rng(seed)

    target_path = np.asarray(
        target_path,
        dtype=int
    )

    T = len(target_path)

    matches = 0

    for _ in range(n_simulations):

        # Draw a fresh seed for each simulation
        sim_seed = rng.integers(
            0,
            2**32 - 1
        )

        simulated_path = simulate_markov(
            P=P,
            T=T,
            pi0=pi0,
            seed=sim_seed
        )

        if np.array_equal(
            simulated_path,
            target_path
        ):
            matches += 1

    return matches / n_simulations

print("nTHEORETICAL VS MONTE CARLO PROBABILITIES")
print("=" * 60)

for label, path in [
    ("a", path_a),
    ("b", path_b),
    ("c", path_c)
]:
    
    theoretical = np.exp(
        markov_loglik(path, P, pi0)
    )

    monte_carlo = estimate_path_frequency(
        target_path=path,
        P=P,
        pi0=pi0,
        n_simulations=100_000,
        seed=42
    )

    print(
        f"Path {label}: "
        f"theoretical = {theoretical:.6f}, "
        f"monte carlo = {monte_carlo:.6f}"
    )