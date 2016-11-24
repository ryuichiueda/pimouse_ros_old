#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse

class MotorTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/motors', nodes, "node does not exist")

    def test_put_freq(self):
        pub = rospy.Publisher('/motor_raw', MotorFreqs)
        m = MotorFreqs()
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

    def test_put_cmd_vel(self):
        pub = rospy.Publisher('/cmd_vel', Twist)
        m = Twist()
        m.linear.x = 0.1414
        m.angular.z = 1.57
        for i in range(10):
            pub.publish(m)
            time.sleep(0.1)

        with open("/dev/rtmotor_raw_l0","r") as f:
            data = f.readline()
            self.assertEqual(data,"200\n","wrong left value from cmd_vel")
        with open("/dev/rtmotor_raw_r0","r") as f:
            data = f.readline()
            self.assertEqual(data,"600\n","wrong right value from cmd_vel")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_motors')
    rostest.rosrun('pimouse_ros','travis_test_motors', MotorTest)
