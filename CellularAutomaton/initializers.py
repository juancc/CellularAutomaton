"""
Functions for initialize volumes

JCA
"""
import numpy as np

def initialize_space(shape, prob=0.5, seed=None):
    """
    Randomly initialize a binary 3D grid with a threshold probability.
    """
    rng = np.random.default_rng(seed)
    return (rng.random(shape) < prob).astype(int)



def initialize_volume_clusters(shape, n_clusters=5, cluster_radius=3, density=0.5, seed=None):
    """
    Generates a 3D initial state for the Game of Life with clustered patterns.

    Parameters:
        shape (tuple): Volume size (x, y, z).
        n_clusters (int): Number of clusters to generate.
        cluster_radius (int): Approximate radius of each cluster.
        density (float): Probability of a voxel being alive inside a cluster (0-1).
        seed (int): Random seed for reproducibility.

    Returns:
        ndarray: Initial 3D binary volume.
    """
    if seed is not None:
        np.random.seed(seed)

    volume = np.zeros(shape, dtype=int)
    X, Y, Z = np.indices(shape)

    for _ in range(n_clusters):
        # Pick a random cluster center
        cx, cy, cz = [np.random.randint(cluster_radius, s - cluster_radius) for s in shape]

        # Generate a sphere mask around the center
        mask = (X - cx)**2 + (Y - cy)**2 + (Z - cz)**2 <= cluster_radius**2

        # Fill inside mask with alive cells at given density
        random_fill = np.random.rand(*shape) < density
        volume[mask & random_fill] = 1

    return volume
