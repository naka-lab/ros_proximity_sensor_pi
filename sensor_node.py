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
    GPIO.output(21, False)
    GPIO.output(20, False)
    time.sleep(1)
     
    # センサーの電源を一つずつonにしてアドレスを設定
    # 21番の電源on
    GPIO.output(21, True)
    time.sleep(1)

    try:
        s = ProximitySensor(0x29)
        s.change_address( 0x10 )
        print( "set GPIO21 to adress:0x10" )
    except:
        print("GPIO21 is ready. ")

    # 20番の電源on
    GPIO.output(20, True)
    time.sleep(1)

    try:
        s = ProximitySensor(0x29)
        s.change_address( 0x11 )
        print( "set GPIO20 to adress:0x11" )
    except:
        print("GPIO20 is ready. ") 


def main():
    set_address()

    rospy.init_node('proximity_sensor')
    
    s1 = ProximitySensor( 0x10 )
    s2 = ProximitySensor( 0x11 )

    pub = rospy.Publisher('proximity_sensor_value', Float32MultiArray, queue_size=1)
    while not rospy.is_shutdown():
        try:
            d1 = s1.get_distance()
            d2 = s2.get_distance()
            print( "distance:", d1, d2 )
            pub.publish( Float32MultiArray(data=[d1, d2]) )
        except IOError:
            print("IOError")

if __name__ == '__main__':
    main()
