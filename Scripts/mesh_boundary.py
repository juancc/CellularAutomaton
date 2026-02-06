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

# stl_path = '/Users/jarbel16/Downloads/sphere/sphere-r1.stl'
# stl_path = '/Users/jarbel16/Downloads/suzanne/suzanne.stl'
stl_path = '/Users/jarbel16/Library/Mobile Documents/com~apple~CloudDocs/Projects/Generative Design/Development/Cellular Automaton/Tests/plant_ball/boundaries1.stl'
# stl_path = '/Users/jarbel16/Library/Mobile Documents/com~apple~CloudDocs/Projects/Generative Design/Development/Cellular Automaton/Tests/sphere/sphere-r1.stl'



SAVEPATH = '/Users/jarbel16/Downloads/' 
SAVEPATH = f'{SAVEPATH}/res-automaton'

STEPS = 200

# Be carefull with the resolution size as
# It handles the domain size
# Large domain can consume all the RAM
# voxel size (same units as STL)
RESOLUTION = 0.001         


def main():
    print(f' - Loading 3D mesh boundary...')
    initial_volume, cmap_dict = init.initialize_volume_clusters_from_stl(
        stl_path,
        # Be carefull with the reso
        resolution=RESOLUTION,
        n_clusters=5, 
        cluster_radius=3, 
        density=0.5,
        noise_density=0.02, 
        env_id=-1,              
        seed=None)


    ##  4555
    rule_fn = life3d_rule_generalized( birth_set={4}, survival_set={5})

    ## Original 5766
    # rule_fn = life3d_rule_generalized( birth_set={5}, survival_set={6})

    volumes = automaton.evolve_volume(initial_volume, rule_fn, steps=STEPS, 
                                    savepath=SAVEPATH, cmap_dict=cmap_dict, 
                                    save_env=False, save_steps=10)


if __name__ == '__main__':
    main()