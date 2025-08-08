"""
Codebook auxfunc

JCA
"""
import numpy as np
from itertools import product
from collections import Counter
import random

def generate_random_codebook(num_rules=3, seed=None):
    rng = np.random.default_rng(seed)
    codebook = {}

    for _ in range(num_rules):
        # Random 3×3×3 binary neighborhood → flatten to 27-element tuple
        neighborhood = rng.integers(0, 2, size=27)
        key = tuple(neighborhood)

        # Assign a new random state (0 or 1)
        new_state = rng.integers(0, 2)
        codebook[key] = new_state

    return codebook


# def life3d_rule(vector):
#     """
#     3D Game of Life rule using the original Conway numbers:
#     - Live cell survives if it has 2 or 3 live neighbours.
#     - Dead cell becomes live if it has exactly 3 live neighbours.
#     """
#     center_index = len(vector) // 2  # automatically find the center
#     center = vector[center_index]
#     neighbors = np.sum(vector) - center  # exclude center from neighbor count

#     if center == 1:
#         return 1 if neighbors in (2, 3) else 0
#     else:
#         return 1 if neighbors == 3 else 0


def life3d_rule(vector):
    """
    3D Game of Life with IDs.
    - Uses original Conway's rules: survival with 2 or 3 neighbors, birth with exactly 3.
    - New cells inherit ID from the majority of neighbors; if no majority, random neighbor's ID.
    """

    center_index = len(vector) // 2
    center_id = int(vector[center_index])

    # Neighbors: exclude center
    neighbor_ids = [int(x) for i, x in enumerate(vector) if i != center_index and x > 0]
    live_count = len(neighbor_ids)  # number of live neighbors

    if center_id > 0:
        # Survival
        return center_id if live_count in (2, 3) else 0
    else:
        # Birth
        if live_count == 3:
            # Pick mode of neighbor IDs
            if neighbor_ids:
                counts = Counter(neighbor_ids)
                most_common = counts.most_common()
                if len(most_common) == 1 or most_common[0][1] > most_common[1][1]:
                    return most_common[0][0]
                else:
                    return random.choice(neighbor_ids)
        return 0