#!/usr/bin/env python

import sys
import unittest, rostest
import rosnode
import time

## A sample python unit test
class BuzzerTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/buzzer',nodes, "node does not exist")

if __name__ == '__main__':
    time.sleep(5)
    rostest.rosrun('raspimouse_ros','test_buzzer',BuzzerTest)
