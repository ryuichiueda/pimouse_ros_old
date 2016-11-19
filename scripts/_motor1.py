#!/usr/bin/env python
import sys, rospy
from std_srvs.srv import SetBool, SetBoolResponse

class Motor():
    def __init__(self):
        if not self.set_power(False): 
            sys.exit(1)

        self.is_on = False
        rospy.on_shutdown(self.set_power)
        self.srv_en = rospy.Service('switch_motors', SetBool, self.callback_en)

    def set_power(self,onoff=False):
        en = "/dev/rtmotoren0"
        try:
            with open(en,'w') as f:
                if onoff: f.write("1\n")
                else:     f.write("0\n")
                self.is_on = onoff
            return True
        except:
            rospy.logerr("cannot write to " + en)

        return False

    def callback_en(self,message):
        d = SetBoolResponse()
        d.success = self.set_power(message.data)
        if self.is_on: d.message = "MOTOR POWER: ON"
        else:          d.message = "MOTOR POWER: OFF"
        return d

if __name__ == '__main__':
    rospy.init_node('motor')
    m = Motor()
    rospy.spin()
