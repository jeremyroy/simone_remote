#!/usr/bin/env python

import roslib; roslib.load_manifest('commands')
import rospy
import tf.transformations
from geometry_msgs.msg import Twist 

def callback(msg):
    rospy.loginfo("Received a \cmd_vel message!")
    rospy.loginfo("Linear components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    rospy.loginfo("Angular components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
    #Jeremy does his magic here 

def receiveTwist():
    rospy.init_node('cmd_vel_listener',anonymous=True)
    rospy.Subscriber("/cmd_vel", Twist, callback)

    rospy.spin() #prevent python from exiting until this node is stopped

if __name__ == '__main__':
    receiveTwist()
