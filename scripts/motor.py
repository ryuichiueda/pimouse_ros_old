#!/usr/bin/env python
import sys, rospy
from std_srvs.srv import SetBool, SetBoolResponse
from pimouse_ros.srv import TimedMotion

class Motor():
    is_on = None

    def __init__(self):
        rospy.on_shutdown(lambda : self.set_power(False))
        self.srv_en = rospy.Service('switch_motors', SetBool, self.callback_en)
        self.srv_tm = rospy.Service('timed_motion', TimedMotion, self.callback_tm)

    def set_power(self,onoff):
        dev = "/dev/rtmotoren0"
        try:
            with open(dev,'w') as f:
                if onoff: f.write("1\n")
                else:     f.write("0\n")
                Motor.is_on = onoff
            return True
        except:
            rospy.logerr("cannot write to " + dev)

        return False

    def callback_en(self,message):
        d = SetBoolResponse()
        d.success = self.set_power(message.data)
        if Motor.is_on: d.message = "MOTOR POWER: ON"
        else:           d.message = "MOTOR POWER: OFF"
        return d

    def callback_tm(self,message):
        if not Motor.is_on:
            rospy.logerr("not enpowered")
            return False

        dev = "/dev/rtmotor0"
        try:
            with open(dev,'w') as f:
                f.write("%d %d %d\n" %
                    (message.left_hz,message.right_hz,message.duration_ms))
        except:
            rospy.logerr("cannot write to " + dev)
            return False
    
        return True

if __name__ == '__main__':
    rospy.init_node('motor')
    m = Motor()
    rospy.spin()
