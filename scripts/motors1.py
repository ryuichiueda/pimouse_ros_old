#!/usr/bin/env python
import sys, rospy
from pimouse_ros.msg import Motion

class Motor():
    def __init__(self):
        if not self.set_power(True): sys.exit(1)

        rospy.on_shutdown(self.set_power)
        self.sub_raw = rospy.Subscriber('motion', Motion, self.callback_raw)

    def set_power(self,onoff=False):
        en = "/dev/rtmotoren0"
        try:
            with open(en,'w') as f:
                f.write("1\n" if onoff else "0\n")
            self.is_on = onoff
            return True
        except:
            rospy.logerr("cannot write to " + en)

        return False

    def callback_raw(self,message):
        if not self.is_on:
            rospy.logerr("not enpowered")
            return

        try:
            lf = open("/dev/rtmotor_raw_l0",'w')
            rf = open("/dev/rtmotor_raw_r0",'w')
            lf.write(str(message.left_hz) + "\n")
            rf.write(str(message.right_hz) + "\n")
        except:
            rospy.logerr("cannot write to rtmotor_raw_*")
    
        lf.close()
        rf.close()

if __name__ == '__main__':
    rospy.init_node('motors')
    m = Motor()
    rospy.spin()
