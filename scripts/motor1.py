#!/usr/bin/env python
import sys, rospy
from std_srvs.srv import SetBool, SetBoolResponse

def callback_motor_sw(message):
    d = SetBoolResponse()

    en0 = "/dev/rtmotoren0"
    try: 
        with open(en0,'w') as f:
            if message.data: f.write("1\n")
            else:            f.write("0\n")
        d.success = True
        d.message = "OK"
    except:
        rospy.logerr("cannot write to " + en0)
        d.success = False
        d.message = "ERROR"

    return d

if __name__ == '__main__':
    rospy.init_node('motor')
    srv = rospy.Service('switch_motors', SetBool, callback_motor_sw)
    rospy.spin()
