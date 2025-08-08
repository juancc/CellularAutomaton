"""
Functions for performing sliding windows over a 3D space

JCA
"""

import numpy as np
from scipy.ndimage import generic_filter
import tqdm

def initialize_space(shape, prob=0.5, seed=None):
    """
    Randomly initialize a binary 3D grid with a threshold probability.
    """
    rng = np.random.default_rng(seed)
    return (rng.random(shape) < prob).astype(int)



def codebook_rule_fn(codebook, not_found='random'):
    """
    Returns a function that applies the codebook rule to a neighborhood vector.

    Parameters:
        codebook (dict): Dictionary mapping 27-bit patterns to new states.
        not_found (str): 'random' or 'l2' strategy.

    Returns:
        function: f(vector) -> new_state
    """
    def rule(vector):
        key = tuple(vector.astype(int))
        if key in codebook:
            return codebook[key]

        if not_found == 'random':
            return np.random.randint(0, 2)
        elif not_found == 'l2':
            keys = np.array(list(codebook.keys()))
            dists = np.sum((keys - vector) ** 2, axis=1)
            return codebook[tuple(keys[np.argmin(dists)])]
        else:
            raise ValueError("not_found must be 'random' or 'l2'.")
    return rule


def apply_rule(volume, rule_fn):
    """
    Applies one step of the cellular automaton using a general rule function.

    Parameters:
        volume (ndarray): 3D binary or multi-state grid.
        rule_fn (function): Function taking a 27-element vector and returning new state.

    Returns:
        new_volume (ndarray): updated volume.
    """
    return generic_filter(volume, rule_fn, size=3, mode='constant', cval=0)


def evolve_volume(initial_volume, rule_fn, steps=10):
    """
    Runs cellular automaton over multiple time steps.

    Parameters:
        initial_volume (ndarray): starting state.
        rule_fn (function): Rule function to apply at each step.
        steps (int): number of time steps.

    Returns:
        List[ndarray]: list of volumes, one per step (including initial).
    """
    print(' - Evolving...')
    volumes = [initial_volume.copy()]
    current = initial_volume.copy()
    for _ in tqdm.tqdm(range(steps), total=steps):
        current = apply_rule(current, rule_fn)
        volumes.append(current.copy())
    return volumes
