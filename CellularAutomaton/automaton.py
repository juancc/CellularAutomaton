"""
Functions for performing sliding windows over a 3D space

JCA
"""
import os
import numpy as np
from scipy.ndimage import generic_filter
import tqdm

import CellularAutomaton.auxfun as aux
import CellularAutomaton.visualization as viz


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


def apply_rule(volume, rule_fn,  window_size=3):
    """
    Applies one step of the cellular automaton using a general rule function.

    Parameters:
        volume (ndarray): 3D binary or multi-state grid.
        rule_fn (function): Function taking a 27-element vector and returning new state.

    Returns:
        new_volume (ndarray): updated volume.
    """
    return generic_filter(volume, rule_fn, size=window_size, mode='constant', cval=0)


# def evolve_volume(initial_volume, rule_fn, steps=10, savepath=None):
#     """
#     Runs cellular automaton over multiple time steps.

#     Parameters:
#         initial_volume (ndarray): starting state.
#         rule_fn (function): Rule function to apply at each step.
#         steps (int): number of time steps.

#     Returns:
#         List[ndarray]: list of volumes, one per step (including initial).
#     """
#     print(' - Evolving...')

#     if savepath:
#         os.makedirs(savepath, exist_ok=True)


#     volumes = [initial_volume.copy()]
#     current = initial_volume.copy()
#     for timestep in tqdm.tqdm(range(steps), total=steps):
#         current = apply_rule(current, rule_fn)

#         if savepath:
#             aux.save_as_pointcloud(current, savepath, timestep)
#             viz.render_as_pointcloud(current, savepath, timestep)

#         volumes.append(current.copy())
#     return volumes


def evolve_volume(initial_volume, rule_fn, steps=10, savepath=None, cmap_dict=None, voxel_size=1.0):
    """
    Runs cellular automaton over multiple time steps.

    Parameters:
        initial_volume (ndarray): starting state with integer IDs per cluster (0 = empty).
        rule_fn (function): Rule function to apply at each step. Must return (volume, cmap_dict).
        steps (int): number of time steps.
        cmap_dict (dict): Optional initial ID→RGB mapping (0–1 floats).
        voxel_size (float): Size of each voxel in plotting/saving.
    """
    print(' - Evolving...')

    if savepath:
        os.makedirs(savepath, exist_ok=True)

    volumes = [initial_volume.copy()]
    current = initial_volume.copy()

    # If no colormap given, generate default mapping from IDs in initial volume
    if cmap_dict is None:
        unique_ids = np.unique(current[current > 0])
        cmap_dict = {int(uid): np.random.rand(3) for uid in unique_ids}
        cmap_dict[0] = (0, 0, 0)  # empty = black

    if savepath:
        # render initial
        aux.save_as_pointcloud(initial_volume, savepath, 0, voxel_size=voxel_size, cmap_dict=cmap_dict)
        viz.render_as_pointcloud(initial_volume, savepath, 0, voxel_size=voxel_size, cmap_dict=cmap_dict)

    for timestep in tqdm.tqdm(range(steps), total=steps):
        # Rule function now returns both the new volume and updated cmap_dict
        # current, cmap_dict = rule_fn(current)
        timestep += 1
        current = apply_rule(current, rule_fn)

        if savepath:
            aux.save_as_pointcloud(current, savepath, timestep, voxel_size=voxel_size, cmap_dict=cmap_dict)
            viz.render_as_pointcloud(current, savepath, timestep, voxel_size=voxel_size, cmap_dict=cmap_dict)

        volumes.append(current.copy())

    return volumes, cmap_dict