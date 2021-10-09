#!/bin/sh

export ROS_MASTER_URI=http://192.168.0.30:11311
export ROS_IP=192.168.0.210

cd ros_proximity_sensor_pi
python sensor_node.py
