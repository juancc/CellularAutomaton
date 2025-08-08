"""
Initial running test

JCA
"""

# Visualization
import CellularAutomaton.visualization as viz
from CellularAutomaton.codebook import generate_random_codebook

# Automaton
import CellularAutomaton.automaton as automaton




# 3D shape
shape = (100, 100, 100)
initial_volume = automaton.initialize_space(shape, prob=0.1)

print(shape[0]*shape[1]*shape[2]*0.1)
print(initial_volume.sum())


# Codebook: All-zero and all-one 3×3×3 blocks
codebook = generate_random_codebook(num_rules=5)
rule = automaton.codebook_rule_fn(codebook, not_found='random')

### Run CA
volumes = automaton.evolve_volume(initial_volume, rule, steps=5)
viz.visualize_volume(volumes[0], mode='voxel')
viz.visualize_volume(volumes[-1], mode='voxel')
