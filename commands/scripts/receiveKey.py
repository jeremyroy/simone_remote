#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Char sent: %s", data.data)

def receiveKey():
    rospy.init_node('receiveKey',anonymous=True)
    rospy.Subscriber("chatter", String, callback)

    rospy.spin() #prevent python from exiting until this node is stopped

if __name__ == '__main__':
    receiveKey()
