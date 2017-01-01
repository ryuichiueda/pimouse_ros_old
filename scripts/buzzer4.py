#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from raspimouse_ros.msg import MusicAction, MusicResult, MusicFeedback

def write_freq(hz):
    bfile = "/dev/rtbuzzer0"
    try:
        with open(bfile,"w") as f:
            f.write(str(hz) + "\n")                
    except IOError:
        rospy.logerr("can't write to " + bfile)

def recv_buzzer(data):
    write_freq(data.data)

def exec_music(goal):
    pass

if __name__ == '__main__':
    rospy.init_node('buzzer')
    rospy.Subscriber("buzzer", UInt16, recv_buzzer)
    music = actionlib.SimpleActionServer('music', MusicAction, exec_music, False)
    rospy.spin()

