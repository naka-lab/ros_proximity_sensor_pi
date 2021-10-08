#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import rospy
from std_msgs.msg import Float32MultiArray
import os
from proximity_sensor import *

os.environ["ROS_MASTER_URI"] = "http://192.168.100.10:11311"
os.environ["ROS_IP"] = "192.168.100.200"

def main():
    #s = ProximitySensor( 0x29 )
    #s.change_address( 0x10 )    
    #return

    rospy.init_node('proximity_sensor')
    
    s1 = ProximitySensor( 0x10 )
    s2 = ProximitySensor( 0x11 )

    pub = rospy.Publisher('proximity_sensor_value', Float32MultiArray, queue_size=10)
    while not rospy.is_shutdown():
        d1 = s1.get_distance()
        d2 = s2.get_distance()
        print( "distance:", d1, d2 )

        pub.publish( Float32MultiArray(data=[d1, d2]) )

if __name__ == '__main__':
    main()
