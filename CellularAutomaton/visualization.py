"""
3D voxels visualization

JCA
"""

import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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
        for pt in points:
            to_draw.append(make_voxel_outline(pt, voxel_size))

    elif mode == 'point':
        to_draw.append(pcd)

    else:
        raise ValueError("Invalid mode. Use 'voxel' or 'point'.")

    o3d.visualization.draw_geometries(to_draw)

