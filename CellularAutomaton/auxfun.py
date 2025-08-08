"""
Auxiliary functions

JCA
"""
import open3d as o3d
import numpy as np
import os
import tqdm


def volume_to_pointcloud(volume, voxel_size=1.0):
    """
    Convert a binary or multi-state 3D volume into a point cloud of coordinates
    where values are non-zero.

    Parameters:
        volume (ndarray): 3D NumPy array.
        voxel_size (float): Scale factor for point spacing.

    Returns:
        points (ndarray): N×3 array of (x, y, z) coordinates.
        values (ndarray): N array of corresponding values from the volume.
    """
    coords = np.argwhere(volume > 0)                     # N × 3
    points = coords.astype(np.float32) * voxel_size      # scaled 3D points
    values = volume[tuple(coords.T)]                     # extract values at those coords
    return points, values



def save_as_pointcloud(volume, filepath, timestep, format='ply', voxel_size=1.0, name = 'points'):
    """Save point cloud. Formats: .ply """
    points, values = volume_to_pointcloud(volume, voxel_size)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    filename = os.path.join(filepath, f'{name}-{timestep}.{format}')

    o3d.io.write_point_cloud(filename, pcd)




