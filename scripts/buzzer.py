#!/usr/bin/env python
from __future__ import print_function
import rospy
from std_msgs.msg import UInt16

def recv_buzzer(data):
	rospy.loginfo(data.data)
	try:
		with open("/dev/rtbuzzer0","w") as f:
			f.print(str(data.data),file=f)
	except:
		rospy.logerr("can't write to /dev/rtbuzzer0")
	

if __name__ == '__main__':
	rospy.init_node('buzzer')
	rospy.Subscriber("buzzer", UInt16, recv_buzzer)
	rospy.spin()

