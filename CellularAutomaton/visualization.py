"""
3D voxels visualization

JCA
"""
import os

import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm
from CellularAutomaton.auxfun import volume_to_pointcloud


def make_voxel_outline(center, size):
    """
    Creates a wireframe cube (LineSet) centered at 'center' with edge length 'size'.
    """
    half = size / 2.0
    corners = np.array([
        [-1, -1, -1],
        [+1, -1, -1],
        [+1, +1, -1],
        [-1, +1, -1],
        [-1, -1, +1],
        [+1, -1, +1],
        [+1, +1, +1],
        [-1, +1, +1],
    ]) * half + center

    lines = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # bottom
        [4, 5], [5, 6], [6, 7], [7, 4],  # top
        [0, 4], [1, 5], [2, 6], [3, 7]   # sides
    ]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(corners)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector([[0, 0, 0]] * len(lines))  # black borders
    return line_set



def visualize_volume(volume, mode='voxel', voxel_size=1.0, color=(0.6, 0.6, 0.6)):
    """
    Visualize a 3D volume as voxel grid or point cloud using Open3D.

    Parameters:
        volume (ndarray): 3D NumPy array.
        mode (str): 'voxel' or 'point'.
        voxel_size (float): Cube/point scale.
        color (tuple): RGB color if not using scalar values.
    """
    points, values = volume_to_pointcloud(volume, voxel_size)

    if len(points) == 0:
        print("No active voxels to display.")
        return

    # Create point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # Assign color
    if np.any(values != values[0]):
        norm_vals = values / np.max(values)
        colors = plt.cm.viridis(norm_vals)[:, :3]
        pcd.colors = o3d.utility.Vector3dVector(colors)
    else:
        pcd.colors = o3d.utility.Vector3dVector(np.tile(color, (len(points), 1)))

    to_draw = []

    if mode == 'voxel':
        # Show filled voxels
        voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)
        to_draw.append(voxel_grid)

        # Add cube edges for shading
        # for pt in points:
        #     to_draw.append(make_voxel_outline(pt, voxel_size))

    elif mode == 'point':
        to_draw.append(pcd)

    else:
        raise ValueError("Invalid mode. Use 'voxel' or 'point'.")

    o3d.visualization.draw_geometries(to_draw)


# def visualize_evolution_voxels_interactive(volumes, cmap='viridis'):
#     """
#     Interactive visualization of 3D cellular automaton using ipywidgets + matplotlib.voxels.

#     Parameters:
#         volumes (List[ndarray]): List of 3D volumes (timesteps).
#         cmap (str): Matplotlib colormap name.
#     """
#     from ipywidgets import interact, IntSlider

#     max_step = len(volumes) - 1
#     shape = volumes[0].shape

#     def plot_step(step):
#         volume = volumes[step]
#         fig = plt.figure(figsize=(6, 6))
#         ax = fig.add_subplot(111, projection='3d')
#         ax.set_title(f"Step {step}")
#         ax.set_xlim(0, shape[0])
#         ax.set_ylim(0, shape[1])
#         ax.set_zlim(0, shape[2])
#         ax.set_box_aspect(shape)
#         ax.set_xticks([])
#         ax.set_yticks([])
#         ax.set_zticks([])

#         filled = volume > 0
#         if np.any(filled):
#             facecolors = np.empty(filled.shape + (4,), dtype=np.float32)
#             norm_vals = volume / volume.max() if volume.max() > 0 else volume
#             colors = cm.get_cmap(cmap)(norm_vals)
#             facecolors[filled] = colors[filled]
#             edgecolors = np.full_like(facecolors, (0, 0, 0, 1))
#             edgecolors[..., :3] = 0  # black borders
#             ax.voxels(filled, facecolors=facecolors, edgecolors=edgecolors)

#         plt.show()

#     interact(plot_step, step=IntSlider(min=0, max=max_step, step=1, value=0))

# def render_evolution_voxels(volumes, path, name='render', cmap='viridis'):
#     """
#     Visualize evolution of a 3D cellular automaton using matplotlib.voxels.

#     Parameters:
#         volumes (List[ndarray]): List of 3D volumes (timesteps).
#         delay (float): Delay between frames in seconds.
#         cmap (str): Matplotlib colormap name for multi-state visualization.
#     """


#     print(' - Rendering')


#     for it in tqdm(enumerate(volumes), total=len(volumes)):
#         t, volume = it

#         fig = plt.figure(figsize=(6, 6))
#         ax = fig.add_subplot(111, projection='3d')
        
#         ax.clear()
#         ax.set_title(f"Step {t}")
#         ax.set_xlim(0, volume.shape[0])
#         ax.set_ylim(0, volume.shape[1])
#         ax.set_zlim(0, volume.shape[2])
#         ax.set_box_aspect(volume.shape)
#         ax.set_xticks([])
#         ax.set_yticks([])
#         ax.set_zticks([])

#         filled = volume > 0
#         if np.any(filled):
#             facecolors = np.empty(filled.shape + (4,), dtype=np.float32)
#             norm_vals = volume / volume.max() if volume.max() > 0 else volume
#             colors = plt.cm.get_cmap(cmap)(norm_vals)
#             facecolors[filled] = colors[filled]
#             edgecolors = np.full_like(facecolors, (0, 0, 0, 1))
#             edgecolors[..., :3] = 0  # black borders
#             ax.voxels(filled, facecolors=facecolors, edgecolors=edgecolors)

#             filepath = os.path.join(path, f'{name}-{t}.png')

#             plt.savefig(filepath )
#             plt.close(fig)



def render_as_pointcloud(volume, path, timestep, name='render', voxel_size=1.0, figsize=(8, 8), colorbar=False):

    points, values = volume_to_pointcloud(volume, voxel_size)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                    c=values, cmap='viridis', s=2, alpha=0.7)
    
    if colorbar: fig.colorbar(sc, ax=ax, label='Voxel Value')
    
    ax.set_axis_off()

    plt.tight_layout()
    
    filename = os.path.join(path, f'{name}-{timestep}.png')
    plt.savefig(filename, dpi=300)
    plt.close(fig)


