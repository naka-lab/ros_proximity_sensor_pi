#!/usr/bin/env python
# encoding: utf8
from __future__ import print_function, unicode_literals
import rospy
from std_msgs.msg import Float32MultiArray
import os
from proximity_sensor import *
import RPi.GPIO as GPIO

#os.environ["ROS_MASTER_URI"] = "http://192.168.100.10:11311"
#os.environ["ROS_IP"] = "192.168.100.200"

def set_address():
    GPIO.setmode(GPIO.BCM)
    
    # すべて電源をoff
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(21, False)
    GPIO.output(20, False)
    GPIO.output(16, False)
    time.sleep(1)

    # センサーの電源を一つずつonにしてアドレスを設定
    turn_on_sensor( 21, 0x10 )
    turn_on_sensor( 20, 0x11 )
    turn_on_sensor( 16, 0x12 )


def main():
    set_address()

    rospy.init_node('proximity_sensor')
    
    s1 = ProximitySensor( 0x10 )
    s2 = ProximitySensor( 0x11 )
    s3 = ProximitySensor( 0x12 )


    pub = rospy.Publisher('proximity_sensor_value', Float32MultiArray, queue_size=1)
    while not rospy.is_shutdown():
        try:
            d1 = s1.get_distance()
            d2 = s2.get_distance()
            d3 = s3.get_distance()
            print( "distance:", d1, d2, d3 )
            pub.publish( Float32MultiArray(data=[d1, d2, d3]) )
        except IOError:
            print("IOError")

if __name__ == '__main__':
    main()
