from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'FeatureLIOM'

setup(
    name = "FeatureLIOM",
    version = "0.0.1",
    packages = find_packages(),
    package_data = {
        'FeatureLIOM': ['config/*.yaml', 'checkpoints/*']
    },
    install_requires = ['setuptools'],
    zip_safe = True,
    maintainer = 'Zihao Dong',
    maintainer_email = 'dong.zih@northeastern.edu',
    description = "Dense Learned Compression for SLAM",
    license = "MIT",
    entry_points = {
        'console_scripts': [
            'keypoint_node = keypoint_node.keypoint_node:main',
        ],
    },
    data_files=[
        ('share/FeatureLIOM/launch', glob('launch/*.launch.py')),
        ('share/FeatureLIOM', ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
)