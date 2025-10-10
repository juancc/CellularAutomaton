"""
Functions for initialize volumes

JCA
"""
import numpy as np
import random 
import trimesh



def initialize_space(shape, prob=0.5, seed=None, col= (0.8, 0.8,0.8)):
    """
    Randomly initialize a binary 3D grid with a threshold probability.
    """
    rng = np.random.default_rng(seed)
    id_to_color = {1: col}


    return (rng.random(shape) < prob).astype(int), id_to_color


def initialize_volume_clusters(
    shape, 
    n_clusters=5, 
    cluster_radius=3, 
    density=0.5,
    noise_density=0.02, 
    env_type=None,             # None, "speckles", or "structured"
    env_density=0.05,          # fraction for speckles
    env_thickness=1,           # thickness for structured planes
    env_id=-1,                 # fixed ID for environment
    seed=None
):
    """
    Generates a 3D initial state for the Game of Life with clusters, noise,
    and optional static environment cells.

    For "structured" env_type:
        Creates several randomly placed small planes of random dimensions/orientation.
    """
    if seed is not None:
        np.random.seed(seed)

    volume = np.zeros(shape, dtype=int)
    color_map = {}
    X, Y, Z = np.indices(shape)

    current_id = 1

    # --- Generate clusters ---
    for _ in range(n_clusters):
        cx, cy, cz = [np.random.randint(cluster_radius, s - cluster_radius) for s in shape]
        mask = (X - cx)**2 + (Y - cy)**2 + (Z - cz)**2 <= cluster_radius**2
        random_fill = np.random.rand(*shape) < density * random.random()
        cluster_mask = mask & random_fill
        volume[cluster_mask] = current_id
        color_map[current_id] = tuple(np.random.rand(3))
        current_id += 1

    # --- Add noise ---
    if noise_density is not None and noise_density > 0:
        noise_mask = (np.random.rand(*shape) < noise_density) & (volume == 0)
        noise_ids = np.where(noise_mask)
        for i in range(len(noise_ids[0])):
            volume[noise_ids[0][i], noise_ids[1][i], noise_ids[2][i]] = current_id
            color_map[current_id] = tuple(np.random.rand(3))
            current_id += 1

    # --- Add environment ---
    if env_type is not None:
        if env_type == "speckles":
            env_mask = (np.random.rand(*shape) < env_density) & (volume == 0)

        elif env_type == "structured":
            env_mask = np.zeros(shape, dtype=bool)
            num_planes = np.random.randint(3, 8)  # number of random planes
            for _ in range(num_planes):
                axis = np.random.choice([0, 1, 2])  # orientation
                # Random size (at least 3×3)
                size_a = np.random.randint(3, shape[(axis + 1) % 3] // 2)
                size_b = np.random.randint(3, shape[(axis + 2) % 3] // 2)

                # Random start so it fits
                start_a = np.random.randint(0, shape[(axis + 1) % 3] - size_a)
                start_b = np.random.randint(0, shape[(axis + 2) % 3] - size_b)

                pos = np.random.randint(0, shape[axis])  # plane position

                if axis == 0:  # plane normal to X
                    env_mask[pos:pos+env_thickness, start_a:start_a+size_a, start_b:start_b+size_b] = True
                elif axis == 1:  # plane normal to Y
                    env_mask[start_a:start_a+size_a, pos:pos+env_thickness, start_b:start_b+size_b] = True
                else:  # axis == 2, plane normal to Z
                    env_mask[start_a:start_a+size_a, start_b:start_b+size_b, pos:pos+env_thickness] = True

            env_mask &= (volume == 0)

        else:
            env_mask = None

        if env_mask is not None and np.any(env_mask):
            volume[env_mask] = env_id
            color_map[env_id] = (0.0, 0.0, 0.0)  # Black

    return volume, color_map



def initialize_volume_clusters_from_stl(
    stl_path,
    resolution=1.0,         # voxel size (same units as STL)
    n_clusters=5, 
    cluster_radius=3, 
    density=0.5,
    noise_density=0.02, 
    env_id=-1,              
    seed=None
):
    """
    Initialize a 3D volume from an STL mesh:
      - domain defined by STL (inside = usable region)
      - environment cells placed on surface
      - clusters and noise generated only inside domain

    Args:
        stl_path (str): Path to STL file
        resolution (float): voxel size (e.g. 1.0 = 1 mm/voxel)
        n_clusters (int): number of clusters
        cluster_radius (int): cluster radius in voxels
        density (float): fill density for clusters
        noise_density (float): probability of random noise voxels
        env_id (int): label for environment voxels (surface)
        seed (int or None): RNG seed

    Returns:
        volume (3D np.array), color_map (dict)
    """
    rng = np.random.default_rng(seed)

    # --- Load mesh ---
    mesh = trimesh.load(stl_path)
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = mesh.dump().sum()

    # --- Compute voxel grid shape from bounding box ---
    min_corner, max_corner = mesh.bounds
    size = max_corner - min_corner
    shape = np.ceil(size / resolution).astype(int) + 1

    print(f' - Domain size: {shape}')


    # --- Build grid coordinates ---
    X, Y, Z = np.indices(shape)
    pts = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)
    pts_world = pts * resolution + min_corner  # map voxel indices to mesh coords

    # --- Determine inside voxels ---
    inside = mesh.contains(pts_world).reshape(shape)

    # --- Initialize volume ---
    volume = np.zeros(shape, dtype=int) + env_id
    volume[inside] = 0  # mark usable domain

    color_map = {}
    current_id = 1

    # --- Generate clusters (only inside mesh) ---
    X, Y, Z = np.indices(shape)
    domain_mask = volume == 0

    for _ in range(n_clusters):
        candidates = np.argwhere(domain_mask)
        if len(candidates) == 0:
            break
        cx, cy, cz = candidates[rng.integers(len(candidates))]

        mask = (X - cx)**2 + (Y - cy)**2 + (Z - cz)**2 <= cluster_radius**2
        random_fill = rng.random(shape) < density * random.random()
        cluster_mask = mask & random_fill & domain_mask

        volume[cluster_mask] = current_id
        color_map[current_id] = tuple(rng.random(3))
        current_id += 1

    # --- Add noise (only inside mesh) ---
    if noise_density is not None and noise_density > 0:
        noise_mask = (rng.random(shape) < noise_density) & domain_mask & (volume == 0)
        noise_indices = np.argwhere(noise_mask)
        for idx in noise_indices:
            x, y, z = idx
            volume[x, y, z] = current_id
            color_map[current_id] = tuple(rng.random(3))
            current_id += 1

    # Assign color for environment
    color_map[env_id] = (0.0, 0.0, 0.0)

    return volume, color_map