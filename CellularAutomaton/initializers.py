"""
Functions for initialize volumes

JCA
"""
import numpy as np

def initialize_space(shape, prob=0.5, seed=None, col= (0.8, 0.8,0.8)):
    """
    Randomly initialize a binary 3D grid with a threshold probability.
    """
    rng = np.random.default_rng(seed)
    id_to_color = {1: col}


    return (rng.random(shape) < prob).astype(int), id_to_color



# def initialize_volume_clusters(shape, n_clusters=5, cluster_radius=3, density=0.5, seed=None):
#     """
#     Generates a 3D initial state for the Game of Life with clustered patterns.

#     Parameters:
#         shape (tuple): Volume size (x, y, z).
#         n_clusters (int): Number of clusters to generate.
#         cluster_radius (int): Approximate radius of each cluster.
#         density (float): Probability of a voxel being alive inside a cluster (0-1).
#         seed (int): Random seed for reproducibility.

#     Returns:
#         ndarray: Initial 3D binary volume.
#     """
#     if seed is not None:
#         np.random.seed(seed)

#     volume = np.zeros(shape, dtype=int)
#     X, Y, Z = np.indices(shape)

#     for _ in range(n_clusters):
#         # Pick a random cluster center
#         cx, cy, cz = [np.random.randint(cluster_radius, s - cluster_radius) for s in shape]

#         # Generate a sphere mask around the center
#         mask = (X - cx)**2 + (Y - cy)**2 + (Z - cz)**2 <= cluster_radius**2

#         # Fill inside mask with alive cells at given density
#         random_fill = np.random.rand(*shape) < density
#         volume[mask & random_fill] = 1

#     return volume

def initialize_volume_clusters(shape, n_clusters=5, cluster_radius=3, density=0.5, seed=None):
    """
    Generates a 3D initial state for the Game of Life with clustered patterns, 
    where each cluster has a unique ID instead of binary states. Includes density control.

    Parameters:
        shape (tuple): Volume size (x, y, z).
        n_clusters (int): Number of clusters to generate.
        cluster_radius (int): Approximate radius of each cluster.
        density (float): Probability of a voxel being alive inside a cluster (0-1).
        seed (int): Random seed for reproducibility.

    Returns:
        volume (ndarray): 3D integer volume where 0 = dead cell, >0 = cluster ID.
        id_to_color (dict): Mapping of cluster IDs to RGB colors.
    """
    if seed is not None:
        np.random.seed(seed)

    volume = np.zeros(shape, dtype=int)
    X, Y, Z = np.indices(shape)
    id_to_color = {}

    for cluster_id in range(1, n_clusters + 1):
        # Pick random cluster center
        cx, cy, cz = [np.random.randint(cluster_radius, s - cluster_radius) for s in shape]

        # Sphere mask for the cluster
        mask = (X - cx)**2 + (Y - cy)**2 + (Z - cz)**2 <= cluster_radius**2

        # Random fill inside mask according to density
        random_fill = np.random.rand(*shape) < density

        # Assign cluster ID to alive cells in this mask
        volume[mask & random_fill] = cluster_id

        # Assign random RGB color for this cluster
        id_to_color[cluster_id] = tuple(np.random.rand(3))

    return volume, id_to_color
