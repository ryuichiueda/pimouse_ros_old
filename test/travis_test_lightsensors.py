#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import LightSensorValues

class LightsensorTest(unittest.TestCase):
    def setUp(self):
        self.count = 0
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self,data):
        self.count += 1
        self.lf = data.left_forward
        self.ls = data.left_side
        self.rs = data.right_side
        self.rf = data.right_forward

    def check_values(self,lf,ls,rs,rf):
        self.assertEqual(self.lf,lf,"different value: left_forward")
        self.assertEqual(self.ls,ls,"different value: left_side")
        self.assertEqual(self.rs,rs,"different value: right_side")
        self.assertEqual(self.rf,rf,"different value: right_forward")

    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/lightsensors',nodes, "node does not exist")

    def test_get_value(self):
        rospy.set_param('lightsensors_freq',10)
        time.sleep(2)
        with open("/dev/rtlightsensor0","w") as f:
            f.write("-1 0 123 4321\n")

        time.sleep(3)
        self.check_values(4321,123,0,-1)

    def test_change_parameter(self):
        rospy.set_param('lightsensors_freq',1)
        time.sleep(2)
        c_prev = self.count
        time.sleep(3)
        self.assertTrue(self.count < c_prev + 4,"freq does not change")
        self.assertFalse(self.count == c_prev,"subscriber is stopped")
        
if __name__ == '__main__':
    rospy.init_node('travis_test_lightsensors')
    rostest.rosrun('pimouse_ros','travis_test_lightsensors',LightsensorTest)
