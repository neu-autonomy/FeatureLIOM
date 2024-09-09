# LiDAR Inertial Odometry and Mapping Using Learned Registration-Relevant Features

## Update

* Code for feature extraction (Python) coming soon!
* Code for DLIOM (C++) will be released separately.
* Our paper is submitted for publication at the IEEE International Conference on Robotics and Automation (ICRA) 2025.

## About

This repository contains the official implementation of the feature extractor network and ros2 node proposed in paper "LiDAR Inertial Odometry and Mapping Using Learned Registration-Relevant Features". It achieves robust and efficient real-time LiDAR Inertial Odometry using a light-weight neural network based feature extractor, as opposed to previous feature-based methods that relies on hand-crafted heuristics and parameters. More detailed maps are shown in the last section.

<br>
<p align='center'>
    <img src="./images/map_neu.png" alt="NEU Campus" width="360" height="230"/>
    <img src="./images/map.png" alt="Newer College Short" width="300"  height="230"/>
</p>

## Dependencies

**Coming Soon**

## Prerequisite

**Coming Soon**

## Running

**Coming Soon**

## Other Datasets

**Comingn Soon**

## Generated Maps

We present detailed maps of the Northeastern University Campus and Newer College Dataset in this section.

### Newer College Dataset

| Sequence      |   RMSE   | Resident Set Size (GB) |   Runtime (ms)  |
| --------      | -------- | ---------------------- | --------------- |
|   Short       |   0.409  |          5.45          |     36.64       |
|   Mount       |   0.195  |          3.99          |     35.67       |
|   Spin        |   0.109  |          0.74          |     41.85       |
|   Quad w. Dyn |   0.147  |          1.71          |     37.07       |
|   Long        |   0.398  |          6.59          |     39.52       |
|   Quad Easy   |   0.072  |          1.68          |     48.30       |
|   Quad Medium |   0.069  |          1.55          |     44.49       |
|   Quad Hard   |   0.065  |          2.21          |     35.58       |
|   Math Easy   |   0.099  |          2.34          |     44.58       |
|   Math Medium |   0.153  |          2.54          |     43.33       |
|   Math Hard   |   0.077  |          2.77          |     42.12       |
|   Cloister    |   0.092  |          5.19          |     24.3        |
|   Park        |   0.342  |          8.52          |     47.03       |


| <img src="./images/newer_college/short.png" width="360"/> | <img src="./images/newer_college/long.png" width="360"/> |
| ----- | ----- |
| *Newer College Short* | *Newer College Long* |

| <img src="./images/newer_college/mount.png" width="360"/> | <img src="./images/newer_college/park.png" width="360"/> |
| ----- | ----- |
| *Newer College Mount* | *Newer College Park* |

| <img src="./images/newer_college/quad_w_dyn.png" width="360"/> | <img src="./images/newer_college/quad_hard.png" width="360" height="237"/> |
| ----- | ----- |
| *Newer College Quad with Dynamics* | *Newer College Quad Hard* |

| <img src="./images/newer_college/quad_medium.png" width="360"/> | <img src="./images/newer_college/quad_easy.png" width="360" height="237"/> |
| ----- | ----- |
| *Newer College Quad Medium* | *Newer College Quad Easy* |

| <img src="./images/newer_college/math_easy.png" width="360"/> | <img src="./images/newer_college/math_medium.png" width="360" height="237"/> |
| ----- | ----- |
| *Newer College Math Easy* | *Newer College Math Medium* |

| <img src="./images/newer_college/math_hard.png" width="360"/> | <img src="./images/newer_college/cloister.png" width="360" height="237"/> |
| ----- | ----- |
| *Newer College Math Hard* | *Newer College Cloister* |

### Northeastern University Main Campus (727.50m)

<p align='center'>
    <img src="./images/main_campus/main_campus_map.png" alt="NEU Campus" width="720"/>
</p>

<p align='center'>
    <img src="./images/main_campus/main_campus_zoom_law_school.png" alt="Law School_LED" width="360"/>
    <img src="./images/main_campus/main_campus_zoom_Shillman_Hall.png" alt="Shillman Hall" width="360"/>
</p>

<p align='center'>
    <img src="./images/main_campus/main_campus_zoom_BofA.png" alt="BofA and Forsyth" width="360"/>
    <img src="./images/main_campus/main_campus_zoom_Forsyth_Sidewalk.png" alt="Forsyth Sidewalk" width="360"/>
</p>

<p align='center'>
    <img src="./images/main_campus/main_campus_zoom_Egan.png" alt="Egan Research Center" width="360"/>
    <img src="./images/main_campus/main_campus_zoom_Egan_Sidewalk.png" alt="Egan Sidewalk" width="360"/>
</p>

<p align='center'>
    <img src="./images/main_campus/main_campus_zoom_Snell.png" alt="Snell Library" width="360"/>
    <img src="./images/main_campus/main_campus_zoom_Willis.png" alt="Willis Hall" width="360"/>
</p>

<p align='center'>
    <img src="./images/main_campus/main_campus_zoom_near_Snell.png" alt="Near Snell Library" width="360"/>
    <img src="./images/main_campus/main_campus_zoom_Willis_car.png" alt="Willis Hall Car" width="360"/>
</p>

<p align='center'>
    <img src="./images/main_campus/main_campus_zoom_painting.png" alt="Painting on Meserve Hall" width="360"/>
    <img src="./images/main_campus/main_campus_zoom_ground_pattern.png" alt="Pattern on ground" width="360"/>
</p>

### Northeastern University ISEC and Columbus Garage (548.32m)

<p align='center'>
    <img src="./images/exp/exp_map.png" alt="NEU ISEC" width="720"/>
</p>

<p align='center'>
    <img src="./images/exp/exp_zoom_bikes.png" width="360"/>
    <img src="./images/exp/exp_zoom_sign_and_pedestrian.png" width="360"/>
</p>

<p align='center'>
    <img src="./images/exp/exp_zoom_parked_cars.png" width="360"/>
    <img src="./images/exp/exp_zoom_columbus_garage.png" width="360"/>
</p>

<p align='center'>
    <img src="./images/exp/exp_zoom_squashbuster.png" width="360"/>
    <img src="./images/exp/exp_zoom_soccer.png" width="360"/>
</p>

<p align='center'>
    <img src="./images/exp/exp_zoom_columbus_back_stairs_and_car.png" width="360"/>
    <img src="./images/exp/exp_zoom_columbus_back.png" width="360"/>
</p>

<p align='center'>
    <img src="./images/exp/exp_zoom_station.png" width="360"/>
    <img src="./images/exp/exp_zoom_bt_isec_and_garage.png" width="360"/>
</p>

<p align='center'>
    <img src="./images/exp/exp_zoom_isec.png" width="360"/>
    <img src="./images/exp/exp_zoom_dorm.png" width="360"/>
</p>

### Northeastern University ISEC Bridge

<p align='center'>
    <img src="./images/bridge/bridge_map.png" width="720"/>
</p>

<p align='center'>
    <img src="./images/bridge/bridge_zoom_exp_ramp.png" width="360"/>
    <img src="./images/bridge/bridge_zoom_exp_door.png" width="360"/>
</p>

<p align='center'>
    <img src="./images/bridge/bridge_zoom_left.png" width="360"/>
    <img src="./images/bridge/bridge_zoom_right.png" width="360"/>
</p>

## Acknowledgement

We would also like to thank Alexander Estornell, Sahasrajit Anantharamakrishnan, and Yash Mewada for setting up the scout robot hardware, and Hanna Zhang, David Thorne, Yanlong Ma, Kenny Chen, and Nakul Joshi for help with data collection and comments.