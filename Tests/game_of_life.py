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

# Visualization
from CellularAutomaton.visualization import visualize_volume
from CellularAutomaton.codebook import life3d_rule

# Automaton
import CellularAutomaton.automaton as automaton




# 3D shape
shape = (10, 10, 10)
initial_volume = automaton.initialize_space(shape, prob=0.2)

volumes = automaton.evolve_volume(initial_volume, life3d_rule, steps=10)

# print(volumes)

for v in volumes:
    visualize_volume(v, mode='voxel')
