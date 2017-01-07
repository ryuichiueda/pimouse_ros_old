#!/usr/bin/env python

#Copyright (c) 2016 Ryuichi Ueda <ryuichiueda@gmail.com>
#This software is released under the BSD License.

import rospy
from std_msgs.msg import UInt16

def recv_buzzer(data):
    rospy.loginfo(data.data)
    bfile = "/dev/rtbuzzer0"
    try:
        with open(bfile,"w") as f:
            f.write(str(data.data) + "\n")                
    except:
        rospy.logerr("can't write to " + bfile)

if __name__ == '__main__':
    rospy.init_node('buzzer')
    rospy.Subscriber("buzzer", UInt16, recv_buzzer)
    rospy.spin()

