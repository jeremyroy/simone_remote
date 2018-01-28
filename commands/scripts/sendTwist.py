#!/usr/bin/env python

#Instructions
# Download getch using: pip install https://pypi.python.org/packages/source/g/getch/getch-1.0-python2.tar.gz#md5=586ea0f1f16aa094ff6a30736ba03c50
# Change keyboard update rate using: sudo kbdrate -r 30 -d 250
# Intel hardware is limited to 250ms minimum. Need a Sparc system to go below 100ms
# For reference, changing back to original settings: sudo kbdrate -r 10.9 -d 250

import getch
import rospy
import roslib;
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import sys

twist = Twist()

# 'a' and 'd' control angular x axis. 'w' and 's' control angular y axis. 'q' and 'e' control the angular z axis.
switcher = {'a':(0,1,0,0),'d':(0,-1,0,0),'w':(0,0,1,0),'s':(0,0,-1,0),'q':(0,0,0,1),'e':(0,0,0,-1),'h':(0,0,0,0)}

def print_publish(key, arrow_key, pub):
    #Flight modes
    if key == '0': #All motors disabled
        twist.linear.y = 0
    elif key == '1': #Acro mode
        twist.linear.y = 1
    elif key == '2': #Stabilization mode
        twist.linear.y = 2
    elif key == '3': #Autonomous mode
        twist.linear.y = 3
    elif key in switcher:
        val = switcher[key]
        twist.linear.x, twist.angular.x, twist.angular.y, twist.angular.z = val
    else: 
        #Set other to 0 when rising, descending, or if invalid key
        twist.linear.x, twist.angular.x, twist.angular.y, twist.angular.z = (0,0,0,0)
        
        #Manage thrust up or down
        if key == ' ' and twist.linear.z < 1: #Going up 
            twist.linear.z += 0.05
        elif key == '.'and twist.linear.z > 0: #Going down
            twist.linear.z -= 0.05
        #Unknown key. Do not publish anything
        else:
            print("Invalid Key")
    
    #Ready to publish linear and angular values
    rospy.loginfo(twist)
    pub.publish(twist)

#Main function
def sendKey():
    #Set up publisher node
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('sender', anonymous=True)
    rate = rospy.Rate(35)

    #define variables
    arrow_key = 0
    inc = 1 

    while not rospy.is_shutdown():
        #get keyboard input
        key = getch.getch()
        
        #Check for special character and obtain third character
        if ord(key) == 27: #Special character key
            key = getch.getch()
            if ord(key) == 91: #Special character key
                key = getch.getch()
                arrow_key = 1 #Differentiate between capital 'A', 'B', 'C', 'D' and arrow keys
        else:
            arrow_key = 0
        

        #Print and publish keyboard command
        print_publish(key, arrow_key, pub)

        last_key = key #Keep track of last key when holding keyboard key

        #Sleep until next rate
        rate.sleep()

if __name__ == '__main__':
    try:
        sendKey()
    except rospy.ROSInterruptException:
        pass




