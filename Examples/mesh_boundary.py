"""
Uses a STL to define the volume boundary

JCA
"""

import CellularAutomaton.visualization as viz
from CellularAutomaton.codebook import life3d_rule, life3d_rule_generalized
import CellularAutomaton.automaton as automaton
import CellularAutomaton.auxfun as aux
import CellularAutomaton.initializers as init

from CellularAutomaton.auxfun import save_as_pointcloud

SAVEPATH = '/Users/jarbel16/Downloads/' 
STEPS = 10

stl_path = '/Users/jarbel16/Downloads/sphere/sphere-r1.stl'

initial_volume, cmap_dict = init.initialize_volume_clusters_from_stl(
    stl_path,
    resolution=0.1,         # voxel size (same units as STL)
    n_clusters=5, 
    cluster_radius=3, 
    density=0.5,
    noise_density=0.02, 
    env_id=-1,              
    seed=None)

print(initial_volume.shape)

save_as_pointcloud(initial_volume, '/Users/jarbel16/Downloads/sphere', 0, save_env=False)


##  4555
SAVEPATH = f'{SAVEPATH}/sphere_test'
rule_fn = life3d_rule_generalized( birth_set={4}, survival_set={5})

## Original 5766
# rule_fn = life3d_rule_generalized( birth_set={5}, survival_set={6})

volumes = automaton.evolve_volume(initial_volume, rule_fn, steps=STEPS, 
                                  savepath=SAVEPATH, cmap_dict=cmap_dict, save_env=False)