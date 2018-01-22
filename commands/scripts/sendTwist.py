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


switcher = {'a':(1,0,0,0),'d':(-1,0,0,0),'w':(0,1,0,0),'s':(0,-1,0,0),'.':(0,0,0,0),' ':(0,0,1,0),'m':(0,0,-1,0)}
switcher_current = {'a':(1,0,0,0),'d':(-1,0,0,0),'w':(0,1,0,0),'s':(0,-1,0,0),'.':(0,0,0,0),' ':(0,0,1,0),'m':(0,0,-1,0)}

def print_publish(key, arrow_key, pub):
    if key in switcher_current:
        val = switcher_current[key]
        twist.linear.x, twist.linear.y, twist.linear.z, twist.angular.z = val
        rospy.loginfo(twist)
        pub.publish(twist)
    else:
        print("Invalid Key")

    #List of keyboard commands
       # if key == 'a':
       #     send_string = "Roll Left"
       # elif key == 'd':
       #     send_string = "Roll Right"
       # elif key == 'w':
       #     send_string = "Pitch Fwd"
       # elif key == 's':
       #     send_string = "Pitch Rvs"
       # elif key == ' ':
       #     send_string = "Up"
       # elif key == 'm':
       #     send_string = "Down"
       # elif key == 'q':
       #     send_string = "Yaw Left"
       # elif key == 'e':
       #     send_string = "Yaw Right"
       # elif key == 'A' and arrow_key == 1:
       #     send_string = "Up arrow"
       # elif key == 'B' and arrow_key == 1:
       #     send_string = "Down arrow"
       # elif key == 'C' and arrow_key == 1:
       #     send_string = "Right arrow"
       # elif key == 'D' and arrow_key == 1:
       #     send_string = "Left arrow"
       # else:
       #     send_string = "%s - Invalid" %key 
                
    #Publish new key
    #rospy.loginfo(send_string)
    #pub.publish(send_string)

#Main function
def sendKey():
    #Set up publisher node
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('sender', anonymous=True)
    rate = rospy.Rate(35)

    #define variables
    last_key = 0
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
        
        #Is the newest key the same as the last
        if last_key == key: #if yes, then increase dictionary values of that list
            temp_list = [x + inc for x in switcher_current[key]]
            switcher_current[key] = temp_list
            print switcher_current[key]
        else: #Otherwise, revert to original standard values
            switcher_current = switcher.copy()
            print key
            print last_key

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




