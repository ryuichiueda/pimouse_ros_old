#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import LightSensorValues

class LightsensorTest(unittest.TestCase):
    lf,ls,rs,rf = 0,0,0,0
    count = 0
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/lightsensors',nodes, "node does not exist")

    def callback(self,data):
        LightsensorTest.count += 1
        LightsensorTest.lf = data.left_forward
        LightsensorTest.ls = data.left_side
        LightsensorTest.rs = data.right_side
        LightsensorTest.rf = data.right_forward

    def check_values(self,lf,ls,rs,rf):
        self.assertEqual(LightsensorTest.lf,lf,"different value: left_forward")
        self.assertEqual(LightsensorTest.ls,ls,"different value: left_side")
        self.assertEqual(LightsensorTest.rs,rs,"different value: right_side")
        self.assertEqual(LightsensorTest.rf,rf,"different value: right_forward")

    def test_get_value(self):
        with open("/dev/rtlightsensor0","w") as f:
            f.write("-1 0 123 4321\n")

        pub = rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)
        time.sleep(3)
        self.check_values(4321,123,0,-1)

    def test_change_freq(self):
        rospy.set_param('lightsensors_freq',1)
        time.sleep(2)
        c_prev = LightsensorTest.count
        time.sleep(3)
        self.assertTrue(LightsensorTest.count < c_prev + 4,"freq does not change")
        rospy.set_param('lightsensors_freq',10)
        time.sleep(2)
        

if __name__ == '__main__':
    time.sleep(5)
    rospy.set_param('lightsensors_freq',10)
    rospy.init_node('travis_test_lightsensors')
    rostest.rosrun('pimouse_ros','travis_test_lightsensors',LightsensorTest)
