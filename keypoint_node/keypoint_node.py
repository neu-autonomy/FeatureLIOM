#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header, Int32MultiArray
import struct
from sensor_msgs_py import point_cloud2

from ruamel import yaml
import os
import time

import torch
import numpy as np
import open3d as o3d

from model.bimodal_compressor import BimodalCompressor
from model.handcrafted_feature_extractor import compute_smoothness
from model.utils import gridSampling

from rclpy.qos import qos_profile_sensor_data


'''
Read point cloud from newer college dataset ply files
'''
def read_point_cloud(filename):

    pcd = o3d.t.io.read_point_cloud(filename)
    points = pcd.point.positions.numpy()
    dist_to_correspondence = pcd.point.intensities.numpy()

    return points, dist_to_correspondence


class KeypointNode(Node):

    '''
    Parameters:
    pcd_topic            : topic to subscribe to for deskewed point cloud
    downsampled_topic    : topic to publish keypoints to
    cfg                  : config file to load model checkpoint
    mode                 : inference mode, chose from "bimodal", "match", "gicp", and "handcrafted"
    lidar_range          : sensing range of the used LiDAR
    '''
    def __init__(self,
        # pcd_topic="/dliom/odom_node/compress",
        pcd_topic="/ouster/points",
        downsampled_topic="/PointRec/descriptor_cloud",
        use_model=False,
        cfg="src/FeatureLIOM/config/bimodal_NCL_Pretrained_Match.yaml",
        mode="bimodal",
        lidar_range=50.0
    ):

        super().__init__('KeypointNode')

        self.use_model = use_model
        self.mode = mode
        self.range = lidar_range

        if self.mode not in ["match_only", "gicp_only", "bimodal", "handcrafted"]:
            print(f"Unknown compression mode {self.mode}")
            exit(1)

        self.deskewed_sub = self.create_subscription(
            PointCloud2,
            topic=pcd_topic,
            callback=self.pcd_callback,
            qos_profile=qos_profile_sensor_data
        )

        self.compressed_pub = self.create_publisher(
            Int32MultiArray,
            topic=downsampled_topic,
            qos_profile=qos_profile_sensor_data
        )

        self.scan_cnt = 0

        y = yaml.YAML(typ='safe', pure=True)

        self.bimodal_config = y.load(open(cfg, 'r'))

        ckpt_path = "./src/FeatureLIOM/" + self.bimodal_config['ckpt_dir'] + '/' + self.bimodal_config['experiment_name'] + "_best.pth"

        self.bimodal_model = BimodalCompressor(self.bimodal_config)

        if os.path.isfile(ckpt_path) and use_model:
            print(f"Loaded model from {ckpt_path}")
            self.bimodal_model.load_state_dict(torch.load(ckpt_path))

        self.bimodal_model = self.bimodal_model.cuda()
        self.bimodal_model.eval()

        for _ in range(5):
            randinput = torch.rand((1000, 3)).float().cuda()
            _ = self.bimodal_model(randinput, None)

        print("Initialization Finished")
    

    def pcd_callback(self, msg):

        start = time.time()

        point_cloud, rings = self.msg_to_torch_pcd(msg)

        if self.use_model:

            with torch.no_grad():

                all_indices = torch.arange(len(point_cloud)).cuda()

                if self.mode == 'handcrafted':

                    smoothness = compute_smoothness(point_cloud, rings, k=10)

                    # incoming scan is not voxelized
                    # to maintain fair comparison we compute rough number of points if we use 0.25 voxel filter
                    rough_indices = gridSampling(point_cloud, resolution=0.25)
                    rough_num = len(rough_indices)

                    # extract top 5% as edge
                    edge_indices = torch.topk(
                        smoothness, 
                        k = int(0.05*rough_num),
                        largest = True
                    ).indices.flatten()

                    all_indices = torch.arange(0, len(smoothness)).cuda()
                    planar_indices = ~torch.isin(all_indices, edge_indices).cuda()
                    planar_indices = all_indices[planar_indices].flatten()
                    indices = torch.randperm(len(planar_indices))[:int(0.15*rough_num)]

                    # rest = point_cloud[planar_indices]
                    # indices = gridSampling(rest, resolution=1.2)

                    planar_indices = planar_indices[indices]

                    direct_kp_indices = torch.cat([edge_indices, planar_indices])

                else:

                    match_score, gicp_score, _ = self.bimodal_model(point_cloud, None)

                    if self.mode == 'gicp_only':
                        
                        # Only choose top 20% GICP feature points
                        gicp_indices = torch.topk(
                            gicp_score,
                            k = int(0.2*len(gicp_score)),
                            largest = False
                        ).indices.flatten()

                        direct_kp_indices = gicp_indices

                    elif self.mode == 'match_only':
                        
                        # Only choose top 20% Match feature points
                        match_indices = torch.topk(
                            match_score,
                            k = int(0.2*len(match_score)),
                            largest = True
                        ).indices.flatten()

                        direct_kp_indices = match_indices

                    else:
                        
                        # Choose top 10% GICP feature and top 10% Match feature
                        gicp_indices = torch.topk(
                            gicp_score,
                            k = int(0.1*len(gicp_score)),
                            largest = False
                        ).indices.flatten()

                        # to avoid selecting same points
                        match_score[gicp_indices] = torch.min(match_score)

                        match_indices = torch.topk(
                            match_score,
                            k = int(0.1*len(match_score)),
                            largest = True
                        ).indices.flatten()

                        direct_kp_indices = torch.cat([match_indices, gicp_indices])

                    point_norms = torch.norm(point_cloud, dim=1)
                    coverage_indices = point_norms >= 0.90 * self.range
                    coverage_indices = coverage_indices.nonzero().flatten()

                    if len(coverage_indices) >= 0.01 * point_cloud.shape[0]:
                        direct_kp_indices = torch.cat([direct_kp_indices, coverage_indices])

                mask = torch.ones(len(point_cloud), dtype=torch.bool)
                mask[direct_kp_indices] = False
                to_be_compressed = point_cloud[mask]
                # to_be_compressed_score = score[mask]
                # _, once_indices = torch.topk(to_be_compressed_score, int(0.34*len(to_be_compressed_score)))

                to_be_compressed_indices = all_indices[mask]

        else:

            # randomly select 20% points from the dense point cloud
            all_indices = torch.arange(len(point_cloud)).cuda()
            direct_kp_indices = torch.randint(low=0, high=len(point_cloud), size=(int(0.2*len(point_cloud)),)).cuda()

            mask = torch.ones(len(point_cloud), dtype=torch.bool)
            mask[direct_kp_indices] = False
            to_be_compressed = point_cloud[mask]

            # once_indices = torch.randint(low=0, high=len(to_be_compressed), size=(int(0.34*len(to_be_compressed)),)).cuda()
            
            to_be_compressed_indices = all_indices[mask]

        # sample a sparse skeleton point cloud
        sparse_indices = gridSampling(to_be_compressed, resolution=3.5)

        all_indices = torch.hstack([
            direct_kp_indices,
            to_be_compressed_indices[sparse_indices]
        ])
        
        # publish indices of points to keep
        # This implementation is more efficient than sending points directly
        # however it requires the odometry code to maintain the ordering of points
        # until they gets compressed (receive indices from this node)
        published_msg = Int32MultiArray()
        published_msg.data = all_indices.to(torch.int32).tolist()
        self.compressed_pub.publish(published_msg)

        runtime = time.time() - start
        self.scan_cnt += 1

        dense_size = point_cloud.shape[0]
        if self.use_model and self.mode == 'handcrafted':
            dense_size = rough_num

        print(f"original cloud size: {dense_size}, compresed cloud size: {all_indices.shape[0]}. Runtime {runtime}s.")
                

    def msg_to_torch_pcd(self, msg):

        point_cloud = point_cloud2.read_points(
            msg,
            skip_nans=True,
            field_names=["x", "y", "z", "intensity", "t", "ring"],
            reshape_organized_cloud=True
        )

        points = np.hstack([
            point_cloud['x'].reshape(-1, 1),
            point_cloud['y'].reshape(-1, 1),
            point_cloud['z'].reshape(-1, 1)
        ])

        rings = point_cloud['ring'].reshape(-1, 1)

        return torch.from_numpy(points).float().cuda(), torch.from_numpy(rings).float().cuda()
    

    def convert_to_pc2_msg(self, points, frame_id='odom'):

        msg = PointCloud2()
        msg.header = Header(frame_id=frame_id)

        if not points.size == 0:

            # fill in meta data
            msg.height = 1
            msg.width = len(points)
            msg.fields = [
                PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
                PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
                PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1)
            ]
            msg.is_bigendian = False
            msg.point_step = 12
            msg.row_step = 12 * points.shape[0]
            msg.is_dense = False

            # convert numpy points to bytes and pass to msg data
            buffer = []
            for point in points:
                buffer.append(struct.pack('fff', *point))
            msg.data = b''.join(buffer)
        
        return msg
    

def main(
    # pcd_topic="/dliom/odom_node/compress",
    pcd_topic="/ouster/points",
    downsampled_topic="/PointRec/descriptor_cloud",
    use_model=True,
    bimodal_cfg="src/FeatureLIOM/config/bimodal_NCL_Pretrained_Match.yaml",
    mode="bimodal",
    lidar_range=128.0
):
    
    rclpy.init()
    node = KeypointNode(
        pcd_topic, 
        downsampled_topic, 
        use_model, 
        bimodal_cfg,
        mode,
        lidar_range
    )
    rclpy.spin(node)
    rclpy.shutdown()
