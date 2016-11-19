#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import Motion
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.srv import TimedMotion

class MotorTest(unittest.TestCase):
    def setUp(self):
        rospy.wait_for_service('/motor_on')
        rospy.wait_for_service('/motor_off')
        rospy.wait_for_service('/timed_motion')
        on = rospy.ServiceProxy('/motor_on', Trigger)
        ret = on()

    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/motors', nodes, "node does not exist")

    def test_on_off(self):
        off = rospy.ServiceProxy('/motor_off', Trigger)
        ret = off()
        self.assertEqual(ret.success, True, "motor off does not succeeded")
        self.assertEqual(ret.message, "OFF", "motor off wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"0\n","wrong value in rtmotor0 at motor off")

        on = rospy.ServiceProxy('/motor_on', Trigger)
        ret = on()
        self.assertEqual(ret.success, True, "motor on does not succeeded")
        self.assertEqual(ret.message, "ON", "motor on wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"1\n","wrong value in rtmotor0 at motor on")

    def test_put_value_raw(self):
        pub = rospy.Publisher('/motion', Motion)
        m = Motion()
        m.left_hz = 123
        m.right_hz = 456
        for i in range(10):
            pub.publish(m)
            time.sleep(0.1)

        with open("/dev/rtmotor_raw_l0","r") as f:
            data = f.readline()
            self.assertEqual(data,"123\n","value does not written to rtmotor_raw_l0")
        with open("/dev/rtmotor_raw_r0","r") as f:
            data = f.readline()
            self.assertEqual(data,"456\n","value does not written to rtmotor_raw_r0")

    def test_put_value_timed(self):
        tm = rospy.ServiceProxy('/timed_motion', TimedMotion)
        tm(-321,654,1500)
        with open("/dev/rtmotor0","r") as f:
            data = f.readline()
            self.assertEqual(data,"-321 654 1500\n","value does not written to rtmotor0")

if __name__ == '__main__':
    rospy.init_node('travis_test_motors')
    rostest.rosrun('pimouse_ros','travis_test_motors', MotorTest)
