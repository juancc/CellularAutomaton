"""
Generate a codebook for a 3D version of Conway’s Game of Life.
Uses Moore neighborhood (3x3x3), center cell included.
The universe of the Game of Life is an infinite, two-dimensional orthogonal 
grid of square cells, each of which is in one of two possible states, 
live or dead (or populated and unpopulated, respectively). E
very cell interacts with its eight neighbours, which are the cells that are 
horizontally, vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

    - Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    - Any live cell with two or three live neighbours lives on to the next generation.
    - Any live cell with more than three live neighbours dies, as if by overpopulation.
    - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

JCA
"""

"""
Initial running test

JCA
"""
import CellularAutomaton.visualization as viz
from CellularAutomaton.codebook import life3d_rule, life3d_rule_generalized
import CellularAutomaton.automaton as automaton
import CellularAutomaton.auxfun as aux
import CellularAutomaton.initializers as init


print('** Game of Life 3D **')

STEPS = 200
SAVEPATH = '/Users/jarbel16/Downloads/' 
# 3D shape
shape = (50, 50, 50)

### CLusters with random noise and environment
initial_volume, cmap_dict = init.initialize_volume_clusters(shape, n_clusters=7, 
                                                                       cluster_radius=5, 
                                                                       density=0.5,
                                                                       noise_density=0.01,
                                                                       env_type = None, #'structured',
                                                                       env_density = 0.1,
                                                                       )

## Original Conway
# SAVEPATH = f'{SAVEPATH}/game_of_life-original-env'
# rule_fn = life3d_rule_generalized( birth_set={3}, survival_set={2, 3})
# rule_fn = life3d_rule_generalized( birth_set={3}, survival_set={2, 3})

##  4555
SAVEPATH = f'{SAVEPATH}/game_of_life-4555-env2'
rule_fn = life3d_rule_generalized( birth_set={4}, survival_set={5})

## Original 5766
# rule_fn = life3d_rule_generalized( birth_set={5}, survival_set={6})

volumes = automaton.evolve_volume(initial_volume, rule_fn, steps=STEPS, savepath=SAVEPATH, cmap_dict=cmap_dict)

