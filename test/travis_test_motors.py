#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
from std_srvs.srv import Trigger, TriggerResponse

class MotorTest(unittest.TestCase):
    def setUp(self):
        rospy.wait_for_service('/motor_on')
        rospy.wait_for_service('/motor_off')

    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/motors', nodes, "node does not exist")

    def test_on_off(self):
        on = rospy.ServiceProxy('/motor_on', Trigger)
        ret = on()
        self.assertEqual(ret.success, True, "motor on does not succeeded")
        self.assertEqual(ret.message, "ON", "motor on wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"1\n","wrong value in rtmotor0 at motor on")

        off = rospy.ServiceProxy('/motor_off', Trigger)
        ret = off()
        self.assertEqual(ret.success, True, "motor off does not succeeded")
        self.assertEqual(ret.message, "OFF", "motor off wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"0\n","wrong value in rtmotor0 at motor off")

if __name__ == '__main__':
    rospy.init_node('travis_test_motors')
    rostest.rosrun('pimouse_ros','travis_test_motors', MotorTest)
