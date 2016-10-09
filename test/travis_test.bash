#!/bin/bash -exv

set -o pipefail

roscore &
sleep 5
rosrun pimouse_ros buzzer.py 2> ./buzzer.err &
sleep 5

###TEST1: existance of the node###
rosnode list | grep '^/buzzer$'

###TEST2: existance of the topic ###
rostopic list | grep '^/buzzer$'

###TEST3: writing test to device files  ###

buz=/dev/rtbuzzer0
##3.1 when any file doesn't exist
# in this moment we assume that the device files don't exist
rostopic pub -1 '/buzzer' std_msgs/UInt16 1000
grep "[ERROR].*$buz" ./buzzer.err

##3.2 when the file exists
sudo touch $buz
sudo chmod 666 $buz

rostopic pub -1 '/buzzer' std_msgs/UInt16 1234
sleep 5

echo 1234 | diff - $buz
