#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time
from std_msgs.msg import UInt16

class BuzzerTest(unittest.TestCase):
    BZFILE = "/dev/rtbuzzer0"
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/buzzer',nodes, "node does not exist")

    def test_put_value(self):
        pub = rospy.Publisher('/buzzer', UInt16)
        for i in range(10):
            pub.publish(1234)
            time.sleep(0.1)

        with open(BuzzerTest.BZFILE,"r") as f:
            data = f.readline()
            self.assertEqual(data,"1234\n","value does not written to " + BuzzerTest.BZFILE)

if __name__ == '__main__':
    rospy.init_node('travis_test_buzzer')
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)
