#!/usr/bin/env python

#define KEYCODE_R 0x43
#define KEYCODE_L 0x44
#define KEYCODE_U 0x41
#define KEYCODE_D 0x42
#define KEYCODE_Q 0x71

#Instructions
# Download getch using: pip install https://pypi.python.org/packages/source/g/getch/getch-1.0-python2.tar.gz#md5=586ea0f1f16aa094ff6a30736ba03c50
# Change keyboard update rate using: sudo kbdrate -r 30 -d 250
# Intel hardware is limited to 250ms minimum. Need a Sparc system to go below 100ms
# For reference, changing back to original settings: sudo kbdrate -r 10.9 -d 250

import getch
import rospy
from std_msgs.msg import String

def print_publish(key, pub):
    #List of keyboard commands
        if key == 'a':
            send_string = "Roll Left"
        elif key == 'd':
            send_string = "Roll Right"
        elif key == 'w':
            send_string = "Pitch Fwd"
        elif key == 's':
            send_string = "Pitch Rvs"
        elif key == ' ':
            send_string = "Up"
        elif key == 'm':
            send_string = "Down"
        elif key == 'q':
            send_string = "Yaw Left"
        elif key == 'e':
            send_string = "Yaw Right"
        if key == 'A':
            send_string = "Up arrow"
        elif key == 'B':
            send_string = "Down arrow"
        elif key == 'C':
            send_string = "Right arrow"
        elif key == 'D':
            send_string = "Left arrow"
        else:
            send_string = "%s - Invalid" %key
        
        last_key = key #Keep track of last key when holding keyboard key
        
        #Publish new key
        rospy.loginfo(send_string)
        pub.publish(send_string)

def sendKey():
    #Set up publisher node
    pub = rospy.Publisher('chatter', String, queue_size=1)
    rospy.init_node('sender', anonymous=True)
    rate = rospy.Rate(35)

    #define variables
    last_key = 0
    released = "key released"

    while not rospy.is_shutdown():
        #get keyboard input
        key = getch.getch()
        
        #Check for arrow keys
        if ord(key) == 27:
            key = getch.getch()
            if ord(key) == 91:
                key = getch.getch()
            #else: nothing or the node will close
        #else: nothing or the node will close
        
        #Was the key released
        if last_key != key:
            pub.publish(released)
        
        print_publish(key, pub)

        
        #Sleep until next rate
        rate.sleep()

if __name__ == '__main__':
    try:
        sendKey()
    except rospy.ROSInterruptException:
        pass




