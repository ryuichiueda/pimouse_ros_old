#!/usr/bin/env python
import sys, rospy
from std_srvs.srv import SetBool, SetBoolResponse
from pimouse_ros.srv import TimedMotion

def callback_en(message):
    d = SetBoolResponse()

    m0 = "/dev/rtmotoren0"
    try: 
        with open(m0,'w') as f:
            if message.data: f.write("1\n")
            else:            f.write("0\n")
        d.success = True
        d.message = "OK"
    except:
        rospy.logerr("cannot write to " + m0)
        d.success = False
        d.message = "ERROR"

    return d

def callback_tm(message):
    en0 = "/dev/rtmotor0"
    try: 
        with open(en0,'w') as f:
            f.write("%d %d %d\n" %
                (message.left_hz,message.right_hz,message.duration_ms))
    except:
        rospy.logerr("cannot write to " + en0)
        return False

    return True

if __name__ == '__main__':
    rospy.init_node('motor')
    srv_en = rospy.Service('switch_motors', SetBool, callback_en)
    srv_tm = rospy.Service('timed_motion', TimedMotion, callback_tm)
    rospy.spin()
