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
from CellularAutomaton.codebook import life3d_rule
import CellularAutomaton.automaton as automaton
import CellularAutomaton.auxfun as aux
import CellularAutomaton.initializers as init


print('Game of Life 3D')

STEPS = 100
SAVEPATH = '/Users/jarbel16/Downloads/game_of_life/' 
# 3D shape
shape = (200, 200, 200)
# initial_volume = init.initialize_space(shape, prob=0.1)
initial_volume = init.initialize_volume_clusters(shape, n_clusters=5, cluster_radius=5, density=0.5)


volumes = automaton.evolve_volume(initial_volume, life3d_rule, steps=STEPS, savepath=SAVEPATH)

