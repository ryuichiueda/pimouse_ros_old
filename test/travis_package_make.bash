#!/bin/bash -xve

#sync and make
rsync -av ./ ~/catkin_ws/src/raspimouse_ros/
cd ~/catkin_ws
catkin_make
