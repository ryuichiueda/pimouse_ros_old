#!/usr/bin/env python
import sys, rospy
from pimouse_ros.msg import LightSensorValues

freq = rospy.get_param('lightsensors_freq',10)
devfile = '/dev/rtlightsensor0'
rospy.init_node('lightsensors')
pub = rospy.Publisher('lightsensors', LightSensorValues, queue_size=1)

try:
    if freq <= 0.0:
        raise Exception()
    rate = rospy.Rate(freq)
except:
    rospy.logerr("value error: lightsensors_freq")
    sys.exit(1)

while not rospy.is_shutdown():
    try:
        with open(devfile,'r') as f:
            data = f.readline().split()
            d = LightSensorValues()
            d.right_forward = int(data[0])
            d.right_side = int(data[1])
            d.left_side = int(data[2])
            d.left_forward = int(data[3])
            pub.publish(d)
    except:
        rospy.logerr("cannot open " + devfile)

    rate.sleep()
