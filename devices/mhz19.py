# Copyright 2022   Dr. Domenico Suriano (domenico.suriano@enea.it)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#########In this section you should import the necessary libraries.
import serial # mandatory library to import
import struct
import time
################################


#############In this section the necessary constants should be placed. Here below it is an example
CONNECTION_TYPE = "usb" # mandatory string which indicates that the device is interfaced by a serial port. Do not modify this one.

DEVICE_IDENTITY = "mhz19" # mandatory string indicating the device name. Modify it with your device name.

DEVICE_SENSORS = "co2[ppm]"

DEVICE_BAUD_RATE = 9600 
###################################

SERIAL_TIMEOUT = 2
ERR_VAL = "-100"
MAX_NUM_ATTEMPT = 2

###############################################


class Mhz19: 

    def __init__(self):
        ### mandatory variables. Do not modify or cancel them.
        self.identity = DEVICE_IDENTITY # mandatory string setting device identity
        self.connection_type = CONNECTION_TYPE # mandatory string setting device output interface type
        self.sensors = DEVICE_SENSORS # mandatory string indicating the magnitudes measured by the device
        self.baud_rate = DEVICE_BAUD_RATE # mandatory variable setting the baud rate of your device
        self.portname = "" # mandatory string indicating the usb port name temporarily set to Null.
        self.port = None # mandatory variable where it is going to be stored the "serial" object


### mandatory functions. Do not modify or cancel them.
    def getConnectionType(self):
        return self.connection_type

    def getConnectionParams(self):
        return [self.portname,self.baud_rate]

    def getIdentity(self):
        return self.identity

    def setIdentity(self,idstring):
        self.identity = idstring
        
    def getSensors(self):
        return self.sensors

    def terminate(self):
        try:
            self.port.close()
        except:
            return
        
    def __del__(self):
        try:
            self.port.close()
        except:
            return
#########################################################
    

## the mandatory function "connect" check if your device is plugged into the SentinAir serial port.
## It returns 1 if your device is found, 0 if it is not found.
## The mandatory argument to pass to the function is the port name (which is a string
## that is going to be passed by the SentinAir system manager)
## where the function is going to search your device

    def connect(self,portname):
        found = 0
        try:
            self.port = serial.Serial(portname,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
        except Exception as e:
            return found
        num_attempt = 0
        while num_attempt < MAX_NUM_ATTEMPT:
            try:
                time.sleep (0.1)
                result = self.port.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
                s = self.port.read(9)
                if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86 and ord(self.__checksum(s[1:-1])) == s[-1]:
                    val = int(s[2]*256 + s[3])
                    if val > 0 and val < 5000:
                        self.portname = portname 
                        found = 1
                        return found
                num_attempt = num_attempt + 1
            except Exception as e:
                num_attempt = num_attempt + 1
        return found


## the mandatory function sample returns the reading of the magnitudes measured by your device.
## It is mandatory that the measures returned are in a string having fields separated by ";". For example: "2.12;4.32;1.21;0.34"
## The number of fields must be the same of the DEVICE_SENSORS constant. If you have just one field,
## the returned string will be,for example, "2.12"

    def sample(self):
        measures = ""
        try:
            result = self.port.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            s = self.port.read(9)
            if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86 and ord(self.__checksum(s[1:-1])) == s[-1]:
                val = int(s[2]*256 + s[3])
                measures = str(val)
                return measures
            return ERR_VAL
        except Exception as e:
            return ERR_VAL

## Here below you can put other functions specific for your device operation
    def __checksum(self,array):
      cs = sum(array) % 0x100
      if cs == 0:
        return struct.pack('B', 0)
      else:
        return struct.pack('B', 0xff - cs + 1)
###################################################
