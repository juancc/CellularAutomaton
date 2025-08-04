"""
Initial running test

JCA
"""

# Visualization
from CellularAutomaton.visualization import visualize_volume, visualize_evolution_matplotlib
from CellularAutomaton.codebook import generate_random_codebook

# Automaton
import CellularAutomaton.automaton as automaton




# 3D shape
shape = (10, 10, 10)
initial_volume = automaton.initialize_space(shape, prob=0.01)

# Codebook: All-zero and all-one 3×3×3 blocks
codebook = generate_random_codebook(num_rules=5)
rule = automaton.codebook_rule_fn(codebook, not_found='random')

# Run CA
volumes = automaton.evolve_volume(initial_volume, rule, steps=5)


visualize_volume(volumes[0], mode='voxel')
visualize_volume(volumes[-1], mode='voxel')
