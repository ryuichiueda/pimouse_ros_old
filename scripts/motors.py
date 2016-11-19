#!/usr/bin/env python
import sys, rospy
from pimouse_ros.msg import Motion
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.srv import TimedMotion

class Motor():
    def __init__(self):
        if not self.set_power(False): sys.exit(1)

        rospy.on_shutdown(self.set_power)
        self.sub_raw = rospy.Subscriber('motion', Motion, self.callback_raw)
        self.srv_on = rospy.Service('motor_on', Trigger, self.callback_on)
        self.srv_off = rospy.Service('motor_off', Trigger, self.callback_off)
        self.srv_tm = rospy.Service('timed_motion', TimedMotion, self.callback_tm)

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

    def callback_sub(self,onoff):
        d = TriggerResponse()
        d.success = self.set_power(onoff)
        d.message = "ON" if self.is_on else "OFF"
        return d

    def callback_on(self,message): return self.callback_sub(True)
    def callback_off(self,message): return self.callback_sub(False)

    def callback_tm(self,message):
        if not self.is_on:
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
    rospy.init_node('motors')
    m = Motor()
    rospy.spin()
