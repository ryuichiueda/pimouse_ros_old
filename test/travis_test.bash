#!/bin/bash -exv

set -o pipefail

roscore &
sleep 5
rosrun pimouse_ros buzzer.py 2> ./out &
sleep 5

###TEST1: existance of the node###
rosnode list		|
grep '^/buzzer$'

###TEST2: existance of the topic ###
rostopic list		|
grep '^/buzzer$'

###TEST3: writing test to /dev/rtbuzzer0  ###

#3.1 when the file doesn't exist
rostopic pub -1 '/buzzer' std_msgs/UInt16 1000
grep '[ERROR].*/dev/rtbuzzer0' ./out

#3.2 when the file exists
touch /dev/rtbuzzer0
chmod 666 /dev/rtbuzzer0
rostopic pub -1 '/buzzer' std_msgs/UInt16 1234
grep '^1234$' /dev/rtbuzzer0
