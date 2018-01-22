#!/usr/bin/env python
#Based on Hector code

import roslib; #roslib.load_manifest('sender')
import rospy
from geometry_msgs.msg import Twist
import sys

twist = Twist()
switcher = {'a':(1,0,0,0),'d':(-1,0,0,0),'w':(0,1,0,0),'s':(0,-1,0,0),'.':(0,0,0,0),'z':(0,0,1,0),'c':(0,0,-1,0)}

def direction():
    value = raw_input('w,s,a,d,z,c,.: ')
    val = switcher[value]
    twist.linear.x, twist.linear.y, twist.linear.z, twist.angular.z = val
    print twist.linear.x, twist.linear.y, twist.linear.x, twist.angular.z
    flag = 0
    return twist

def send2():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('sender', anonymous=True)
    rate = rospy.Rate(2) 
    while not rospy.is_shutdown():
        twist = direction()
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        send2()
    except rospy.ROSInterruptException:
        pass
