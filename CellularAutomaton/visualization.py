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





# def render_as_pointcloud(volume, path, timestep, name='render', voxel_size=1.0, figsize=(8, 8), colorbar=False):

#     points, values = volume_to_pointcloud(volume, voxel_size)

#     fig = plt.figure(figsize=figsize)
#     ax = fig.add_subplot(111, projection='3d')
    
#     sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2],
#                     c=values, cmap='viridis', s=2, alpha=0.7)
    
#     if colorbar: fig.colorbar(sc, ax=ax, label='Voxel Value')
    
#     ax.set_axis_off()

#     plt.tight_layout()
    
#     filename = os.path.join(path, f'{name}-{timestep}.png')
#     plt.savefig(filename, dpi=300)
#     plt.close(fig)


def render_as_pointcloud(volume, path, timestep, cmap_dict=None,
                         name='render', voxel_size=1.0, figsize=(8, 8), colorbar=False):
    """
    Render a 3D volume as a point cloud with optional fixed colors per ID.

    Parameters:
        volume (ndarray): 3D NumPy array of IDs (0 = empty).
        path (str): Folder to save images.
        timestep (int): Current simulation step.
        cmap_dict (dict): Mapping from ID -> RGB tuple in [0, 1].
        name (str): Base filename for saving.
        voxel_size (float): Scaling for voxel spacing.
        figsize (tuple): Matplotlib figure size.
        colorbar (bool): Show colorbar if True (ignored if cmap_dict given).
    """
    points, values = volume_to_pointcloud(volume, voxel_size)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    if cmap_dict is not None:
        # Map IDs to RGB colors
        colors = np.array([cmap_dict.get(v, (0.5, 0.5, 0.5)) for v in values])
        sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                        c=colors, s=2, alpha=0.7)
    else:
        sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2],
                        c=values, cmap='viridis', s=2, alpha=0.7)
        if colorbar:
            fig.colorbar(sc, ax=ax, label='Voxel Value')

    ax.set_axis_off()
    plt.tight_layout()

    filename = os.path.join(path, f'{name}-{timestep}.png')
    plt.savefig(filename, dpi=300)
    plt.close(fig)
