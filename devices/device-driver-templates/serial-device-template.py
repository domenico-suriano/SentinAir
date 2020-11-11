# Copyright 2020   Dr. Domenico Suriano (domenico.suriano@enea.it)
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
################################


#############In this section the necessary constants should be placed. Here below it is an example
CONNECTION_TYPE = "serial" # mandatory string which indicates that the device is interfaced by a serial port. Do not modify this one.

DEVICE_IDENTITY = "device name chosen by the user" # mandatory string indicating the device name. Modify it with your device name.

# mandatory string indicating the magnitudes measured by the device. It must have fields separated by ";"
# as in the example below
# DEVICE_SENSORS = "NO2[ppb];NO[ppb];NOx[ppb]". Modify it for your device operation.
"""
if you have just one field, then the constant will be:
DEVICE_SENSORS = "NO2[ppb]"
"""
DEVICE_SENSORS = "field1[unit of measure 1];field2[unit of measure 2];field3[unit of measure 3]"

DEVICE_BAUD_RATE = your_device_baud_rate # mandatory integer value indicating the serial communication baud rate
""" for example:
DEVICE_BAUD_RATE = 9600
"""
###################################

#### Here below you can put other constants specific for the operation of your device
""" for example:
SERIAL_TIMEOUT = 2
"""
###############################################


class Serial-device-template: #it is mandatory that the class name must have the same name of the file (serial-device-template.py) with the capital first letter

    def __init__(self):
        ### mandatory variables. Do not modify or cancel them.
        self.identity = DEVICE_IDENTITY # mandatory string setting device identity
        self.connection_type = CONNECTION_TYPE # mandatory string setting device output interface type
        self.sensors = DEVICE_SENSORS # mandatory string indicating the magnitudes measured by the device
        self.baud_rate = DEVICE_BAUD_RATE # mandatory variable setting the baud rate of your device
        self.portname = "" # mandatory string indicating the usb port name temporarily set to Null.
        self.port = None # mandatory variable where it is going to be stored the "serial" object
        ### here below you can put other variables specific for the operation of your device
        
        #################################################


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
            ### put here the code specific for your device
            """ for example:
            self.port = serial.Serial(portname,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
            """
            ###############################
            self.portname = portname ## if your device is found at the passed serial port, the device serial port name is set.
            found = 1
        except Exception as e:
            pass
        return found


## the mandatory function sample returns the reading of the magnitudes measured by your device.
## It is mandatory that the measures returned are in a string having fields separated by ";". For example: "2.12;4.32;1.21;0.34"
## The number of fields must be the same of the DEVICE_SENSORS constant. If you have just one field,
## the returned string will be,for example, "2.12"

    def sample(self):
        measures = ""
        try:
             ### put here the code specific for your device

            ###############################
            return measures.rstrip(";")
        except Exception as e:
            return ""

## Here below you can put other functions specific for your device operation

###################################################
