#!/usr/bin/env python
import sys, rospy
from std_srvs.srv import SetBool, SetBoolResponse

class Motor():
    is_on = None

    def __init__(self):
        rospy.on_shutdown(lambda : self.set_power(False))
        self.srv_en = rospy.Service('switch_motors', SetBool, self.callback_en)

    def set_power(self,onoff):
        en = "/dev/rtmotoren0"
        try:
            with open(en,'w') as f:
                if onoff: f.write("1\n")
                else:     f.write("0\n")
                Motor.is_on = onoff
            return True
        except:
            rospy.logerr("cannot write to " + en)

        return False

    def callback_en(self,message):
        d = SetBoolResponse()
        d.success = self.set_power(message.data)
        if Motor.is_on: d.message = "MOTOR POWER: ON"
        else:           d.message = "MOTOR POWER: OFF"
        return d

if __name__ == '__main__':
    rospy.init_node('motor')
    m = Motor()
    rospy.spin()
