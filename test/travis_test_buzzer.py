#!/usr/bin/env python
import unittest, rostest
import rosnode
import time

class BuzzerTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/buzzer',nodes, "node does not exist")

if __name__ == '__main__':
    time.sleep(5)
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)
