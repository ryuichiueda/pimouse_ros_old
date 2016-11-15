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

        with open(self.BZFILE,"r") as f:
            data = f.readline().rstrip()
            self.assertEqual(data,"1234","value does not written to " + self.BZFILE)

if __name__ == '__main__':
    time.sleep(5)
    rospy.init_node('travis_test_buzzer')
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)
