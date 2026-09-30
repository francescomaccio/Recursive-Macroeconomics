"""
Exercise 2.3

The text of the exercise is already contained in the associated pdf file solution

"""

################### PART B ###################

import numpy as np

def markov_loglik(path, P, pi0):
    path = np.asarray(path, dtype=int)

    probs = [pi0[path[0]]]

    for t in range(len(path) - 1):
        probs.append(
            P[path[t], path[t + 1]]
        )

    probs = np.array(probs)

    if np.any(probs == 0):
        return -np.inf

    return np.log(probs).sum()

def map_to_states(observations, y_values):

    mapping = {
        value: state
        for state, value in enumerate(y_values)
    }

    return np.array(
        [mapping[value] for value in observations],
        dtype=int
    )
    
def CRRA_utility(c, gamma):
    c = np.asarray(c, dtype=float)
    
    return c**(1-gamma)/(1-gamma)

def discounted_value(P, pi0, cbar, beta, gamma):
    """
    Computes:

        u = period utility vector
        v = conditional discounted value vector
        V = unconditional discounted expected utility
    """
    u = CRRA_utility(cbar, gamma)
    
    n = len(cbar)
    
    v = np.linalg.solve(
        np.eye(n) - beta * P,
        u
    )
    
    V = pi0 @ v
    
    return u, v, V

pi0 = np.array([
    0.5,
    0.5
])

P1 = np.array([
    [1.0, 0.0],
    [0.0, 1.0]
])

P2 = np.array([
    [0.5, 0.5],
    [0.5, 0.5]
])

cbar = np.array([
    1.0,
    5.0
])

beta = 0.95

gamma = 4

for name, P in [
    ("Process 1", P1),
    ("Process 2", P2)
]:
    
    u, v, V = discounted_value(
        P=P,
        pi0 = pi0,
        cbar = cbar,
        beta = beta,
        gamma = gamma
    )
    
    print(f"\n{name}")
    print("=" * 50)

    print("Utility vector:")
    print(u)

    print("Conditional value vector:")
    print(v)

    print(f"Unconditional value V = {V:.6f}")
    

gamma = 2.5

for name, P in [
    ("Process 1", P1),
    ("Process 2", P2)
]:
    
    u, v, V = discounted_value(
        P=P,
        pi0 = pi0,
        cbar = cbar,
        beta = beta,
        gamma = gamma
    )
    
    print(f"\n{name}")
    print("=" * 50)

    print("Utility vector:")
    print(u)

    print("Conditional value vector:")
    print(v)

    print(f"Unconditional value V = {V:.6f}")
    
################### PART C ###################

data_c = [
    1,1,1,1,1,
    1,1,1,1,1
]

path_c = map_to_states(
    data_c,
    y_values=[1, 5]
)

for name, P in [
    ("Process 1", P1),
    ("Process 2", P2)
]:

    loglik = markov_loglik(
        path_c,
        P,
        pi0
    )

    likelihood = np.exp(loglik)

    print(
        f"{name}: "
        f"log-likelihood = {loglik:.6f}, "
        f"likelihood = {likelihood:.10f}"
    )
    
################### PART D ###################

def posterior_model_probs(
    path,
    models,
    pi0,
    priors
):
    """
    Bayesian posterior probabilities over competing Markov models.
    models:
        dictionary of transition matrices

    priors:
        array of prior probabilities
    """
    
    logliks = np.array([
        markov_loglik(
            path,
            P,
            pi0
        )
        for P in models.values()
    ])
    
    likelihoods = np.exp(logliks)
    
    numerators = (
        likelihoods *
        np.asanyarray(priors)
    )
    
    posteriors = (
        numerators/
        numerators.sum()
    )
    
    return likelihoods, posteriors

models = {
    "Process 1": P1,
    "Process 2": P2,
}

priors = np.array([
    0.5, 
    0.5
])

likelihoods, posteriors = posterior_model_probs(
    path= path_c,
    models=models,
    pi0=pi0,
    priors=priors
)

for name, likelihood, posterior in zip(
    models.keys(),
    likelihoods,
    posteriors
):
    
    print(
        f"{name}:"
        f"L = {likelihood:.10f},"
        f"Posterior = {posterior:.6f}"
    )
    
################### PART E ###################

data_e = [
    1, 5, 5, 1, 5,
    5, 1, 5, 1, 5
]

path_e = map_to_states(
    data_e,
    y_values=[1, 5]
)

likelihoods, posteriors = posterior_model_probs(
    path=path_e,
    models=models,
    pi0=pi0,
    priors=priors
)

for name, likelihood, posterior in zip(
    models.keys(),
    likelihoods,
    posteriors
):

    print(
        f"{name}: "
        f"L = {likelihood:.10f}, "
        f"Posterior = {posterior:.6f}"
    )
    
################### EXTENSION 1 - SEQUENTIAL BAYESIAN LEARNING ###################

def sequential_posteriors(
    observations,
    models,
    pi0,
    priors,
    y_values
):

    states = map_to_states(
        observations,
        y_values
    )

    results = []

    for T in range(1, len(states) + 1):

        partial_path = states[:T]

        likelihoods, posteriors = posterior_model_probs(
            path=partial_path,
            models=models,
            pi0=pi0,
            priors=priors
        )

        results.append(
            (
                T,
                likelihoods.copy(),
                posteriors.copy()
            )
        )

    return results

seq_results = sequential_posteriors(
    observations=data_c,
    models=models,
    pi0=pi0,
    priors=priors,
    y_values=[1, 5]
)

print(
    "T | Posterior M1 | Posterior M2"
)

print("-" * 40)

for T, _, posterior in seq_results:

    print(
        f"{T:2d} | "
        f"{posterior[0]:.6f}     | "
        f"{posterior[1]:.6f}"
    )
    
################### EXTENSION 2 - CONSUMPTION PERSISTENCE AND AUTOCORRELATION ###################


def theoretical_autocorrelation(
    P,
    pi,
    values,
    max_lag=5
):

    values = np.asarray(
        values,
        dtype=float
    )

    mean = pi @ values

    variance = (
        pi @ (values**2)
        - mean**2
    )

    correlations = []

    for k in range(
        1,
        max_lag + 1
    ):

        joint_moment = (
            pi
            @ np.diag(values)
            @ np.linalg.matrix_power(P, k)
            @ values
        )

        covariance = (
            joint_moment
            - mean**2
        )

        correlation = (
            covariance /
            variance
        )

        correlations.append(
            correlation
        )

    return np.array(correlations)

for name, P in models.items():

    rho = theoretical_autocorrelation(
        P=P,
        pi=pi0,
        values=cbar,
        max_lag=5
    )

    print(
        f"\n{name}"
    )

    for lag, value in enumerate(
        rho,
        start=1
    ):

        print(
            f"Lag {lag}: "
            f"{value:.3f}"
        )
        
################### EXTENSION 3 - EXPECTED DURATION OF CONSUMPTION REGIMES ###################


def expected_spell_duration(P):

    durations = []

    for i in range(
        P.shape[0]
    ):

        persistence = P[i, i]

        if np.isclose(
            persistence,
            1.0
        ):

            duration = np.inf

        else:

            duration = (
                1 /
                (1 - persistence)
            )

        durations.append(
            duration
        )

    return np.array(durations)

for name, P in models.items():

    durations = expected_spell_duration(
        P
    )

    print(
        f"\n{name}"
    )

    print(
        f"Low-consumption expected duration : "
        f"{durations[0]}"
    )

    print(
        f"High-consumption expected duration: "
        f"{durations[1]}"
    )
    
################### EXTENSION 4 - CERTAINTY-EQUIVALENT CONSUMPTION ###################
    
def certainty_equivalent(
    V,
    beta,
    gamma
):

    lifetime_adjusted_utility = (
        (1 - beta) * V
    )

    c_ce = (
        (1 - gamma)
        * lifetime_adjusted_utility
    ) ** (
        1 /
        (1 - gamma)
    )

    return c_ce

for gamma in [
    2.5,
    4
]:

    print(
        f"\ngamma = {gamma}"
    )

    for name, P in models.items():

        _, _, V = discounted_value(
            P=P,
            pi0=pi0,
            cbar=cbar,
            beta=beta,
            gamma=gamma
        )

        ce = certainty_equivalent(
            V=V,
            beta=beta,
            gamma=gamma
        )

        print(
            f"{name}: "
            f"V = {V:.6f}, "
            f"CE consumption = {ce:.6f}"
        )