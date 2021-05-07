#!/usr/bin/python
# encoding: utf8

import time
import smbus

VL6180X_SYSTEM_FRESH_OUT_OF_RESET = 0x0016
VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME = 0x001C
VL6180X_SYSRANGE_RANGE_CHECK_ENABLES = 0x002D
VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE = 0x0022
VL6180X_SYSALS_INTEGRATION_PERIOD = 0x0040
VL6180X_SYSALS_ANALOGUE_GAIN = 0x3F
VL6180X_FIRMWARE_RESULT_SCALER = 0x0120
VL6180X_SYSRANGE_START = 0x0018
VL6180X_RESULT_RANGE_VAL = 0x0062
VL6180X_SYSTEM_INTERRUPT_CLEAR = 0x0015
VL6180X_SYSALS_START = 0x0038
VL6180X_RESULT_ALS_VAL = 0x0050


class ProximitySensor():
    bus = smbus.SMBus(1)

    def __init__(self, addr ):
        self.addr = addr
        self.init_sensor()
    

    def init_sensor(self):
        if self.read(VL6180X_SYSTEM_FRESH_OUT_OF_RESET) == 1:
            print "sensor is ready."
            self.writebyte(0x0207, 0x01)
            self.writebyte(0x0208, 0x01)
            self.writebyte(0x0096, 0x00)
            self.writebyte(0x0097, 0xfd)
            self.writebyte(0x00e3, 0x00)
            self.writebyte(0x00e4, 0x04)
            self.writebyte(0x00e5, 0x02)
            self.writebyte(0x00e6, 0x01)
            self.writebyte(0x00e7, 0x03)
            self.writebyte(0x00f5, 0x02)
            self.writebyte(0x00d9, 0x05)
            self.writebyte(0x00db, 0xce)
     
            self.writebyte(0x00dc, 0x03)
            self.writebyte(0x00dd, 0xf8)
            self.writebyte(0x009f, 0x00)
            self.writebyte(0x00a3, 0x3c)
            self.writebyte(0x00b7, 0x00)
            self.writebyte(0x00bb, 0x3c)
            self.writebyte(0x00b2, 0x09)
            self.writebyte(0x00ca, 0x09)
            self.writebyte(0x0198, 0x01)
            self.writebyte(0x01b0, 0x17)
            self.writebyte(0x01ad, 0x00)
            self.writebyte(0x00ff, 0x05)
            self.writebyte(0x0100, 0x05)
            self.writebyte(0x0199, 0x05)
            self.writebyte(0x01a6, 0x1b)
            self.writebyte(0x01ac, 0x3e)
            self.writebyte(0x01a7, 0x1f)
            self.writebyte(0x0030, 0x00)
        #default_settings
        # Recommended : Public registers - See data sheet for more detail
        self.writebyte(0x0011, 0x10); # Enables polling for 'New Sample ready' when measurement completes
        self.writebyte(0x010a, 0x30); # Set the averaging sample period (compromise between lower noise and increased execution time)
        self.writebyte(0x003f, 0x46); # Sets the light and dark gain (upper nibble). Dark gain should not be changed.
        self.writebyte(0x0031, 0xFF); # sets the # of range measurements after which auto calibration of system is performed
        self.writebyte(0x0040, 0x63); # Set ALS integration time to 100ms DocID026571 Rev 1 25/27 AN4545 SR03 settings27
        self.writebyte(0x002e, 0x01); # perform a single temperature calibration of the ranging sensor
         
        #Optional: Public registers - See data sheet for more detail
        self.writebyte(0x001b, 0x09); # Set default ranging inter-measurement period to 100ms
        self.writebyte(0x003e, 0x31); # Set default ALS inter-measurement period to 500ms
        self.writebyte(0x0014, 0x24); # Configures interrupt on 'New Sample Ready threshold event' 
        self.writebyte(0x016, 0x00); #change fresh out of set status to 0
         
        # Additional settings defaults from community
        self.writebyte(VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME, 0x32)
        self.writebyte(VL6180X_SYSRANGE_RANGE_CHECK_ENABLES, 0x10 | 0x01)
        self.writebyte16(VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE, 0x7B)
        self.writebyte16(VL6180X_SYSALS_INTEGRATION_PERIOD, 0x64) #100ms
        self.writebyte(VL6180X_SYSALS_ANALOGUE_GAIN, 0x20) #x40
        self.writebyte(VL6180X_FIRMWARE_RESULT_SCALER, 0x01)

 
 
    def read(self, register16):
        a1 = (register16 >> 8) & 0xFF
        a0 = register16 & 0xFF
        self.bus.write_i2c_block_data(self.addr, a1, [a0])
        return self.bus.read_byte(self.addr)
 
    def read16(self, register16):
        a1 = (register16 >> 8) & 0xFF
        a0 = register16 & 0xFF
        self.bus.write_i2c_block_data(self.addr, a1, [a0])
        data16h = self.bus.read_byte(self.addr)
        data16l = self.bus.read_byte(self.addr)
        return (data16h << 8) | (data16l & 0xFF)
     
    def writebyte(self, register16, data):
        a1 = (register16 >> 8) & 0xFF
        a0 = register16 & 0xFF
        self.bus.write_i2c_block_data(self.addr, a1, [a0, (data & 0xFF)])
     
    def writebyte16(self, register16, data16):
        a1 = (register16 >> 8) & 0xFF
        a0 = register16 & 0xFF
        d1 = (data16 >> 8) & 0xFF
        d0 = data16 & 0xFF
        self.bus.write_i2c_block_data(self.addr, a1, [a0, d1, d0])
        
    def get_distance(self):
        self.writebyte(VL6180X_SYSRANGE_START, 0x01) #0x03 renzoku
        time.sleep(0.1)
        distance = self.read(VL6180X_RESULT_RANGE_VAL)
        self.writebyte(VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)
        #print distance,"mm"
        return distance
        
    def get_light(self):
        self.writebyte(VL6180X_SYSALS_START, 0x01)
        time.sleep(0.5)
        light = self.read16(VL6180X_RESULT_ALS_VAL)
        self.writebyte(VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)
        #print read(VL6180X_SYSALS_ANALOGUE_GAIN)
        #print read16(VL6180X_SYSALS_INTEGRATION_PERIOD)
        print light*0.32*100/(32*100),"lux"
        
    def change_address(self, newaddr):
        self.writebyte( 0x212, newaddr )


def main():
    s1 = ProximitySensor( 0x10 )
    s2 = ProximitySensor( 0x11 )
    #s1.change_address( 0x10 )
    #aaa
    while 1:
        d1 = s1.get_distance()
        d2 = s2.get_distance()
        print d1, d2

if __name__=="__main__":
    main()

