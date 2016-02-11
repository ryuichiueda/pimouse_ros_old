#!/bin/bash -exv

set -o pipefail

roscore &
sleep 5
rosrun pimouse_ros buzzer1.py &
sleep 5

###TEST1: nodes are running or not###
rosnode list		|
grep '^/buzzer$'
