"""
Codebook auxfunc

JCA
"""
import numpy as np
from itertools import product


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
#     Rules function for 3D game of life.
#     The universe of the Game of Life is an infinite, two-dimensional orthogonal 
#     grid of square cells, each of which is in one of two possible states, 
#     live or dead (or populated and unpopulated, respectively). E
#     very cell interacts with its eight neighbours, which are the cells that are 
#     horizontally, vertically, or diagonally adjacent.
    
#     At each step in time, the following transitions occur:

#         - Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#         - Any live cell with two or three live neighbours lives on to the next generation.
#         - Any live cell with more than three live neighbours dies, as if by overpopulation.
#         - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#     """     
#     center = vector[13]
#     neighbors = np.sum(vector) - center
#     if center == 1:
#         return 1 if 5 <= neighbors <= 7 else 0
#     else:
#         return 1 if neighbors == 6 else 0


def life3d_rule(vector):
    """
    3D Game of Life rule using the original Conway numbers:
    - Live cell survives if it has 2 or 3 live neighbours.
    - Dead cell becomes live if it has exactly 3 live neighbours.
    """
    center_index = len(vector) // 2  # automatically find the center
    center = vector[center_index]
    neighbors = np.sum(vector) - center  # exclude center from neighbor count

    if center == 1:
        return 1 if neighbors in (2, 3) else 0
    else:
        return 1 if neighbors == 3 else 0
