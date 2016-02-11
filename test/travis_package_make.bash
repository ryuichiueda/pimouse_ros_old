#!/bin/bash -xve

#required packages
pip install catkin_pkg
pip install empy
pip install pyyaml
pip install rospkg

#sync and make
rsync -av ./ ~/catkin_ws/src/raspimouse_ros/
cd ~/catkin_ws
catkin_make
