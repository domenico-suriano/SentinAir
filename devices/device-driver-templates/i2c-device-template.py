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
""" for example:
from smbus2 import SMBus
"""
################################


#############In this section the mandatory constants should be placed.
CONNECTION_TYPE = "i2c" # mandatory string which indicates that the device is interfaced by a I2C bus. Do not modify this one.

# mandatory list which indicates the possible i2c bus addresses where your device must be searched.
# You can modify it by inserting the values right for your device operation
# following the example below
# I2C_ADDRESSES = [0x68,0x69,0x6A,0x6B,0x6C,0x6D,0x6E,0x6F]
I2C_ADDRESSES = [address1,address2,address3]
#############################################################################

DEVICE_IDENTITY = "device name chosen by the user" # mandatory string indicating the device name. Modify it with your device name.

# mandatory string indicating the magnitudes measured by the device. It must have fields separated by ";"
# as in the example below
# DEVICE_SENSORS = "V1[V];V2[V];V3[V];V4[V]". Modify it for your device operation.
"""
if you have just one field, then the constant will be:
DEVICE_SENSORS = "V1[V]"
"""
DEVICE_SENSORS = "field1[unit of measure 1];field2[unit of measure 2];field3[unit of measure 3];field4[unit of measure 4]"
###################################

#### Here below you can put other constants specific for the operation of your device

###############################################


class I2c-device-template: #it is mandatory that the class name must have the same name of the file (i2c-device-template.py) with the capital first letter

    def __init__(self):
        ### mandatory variables. Do not modify or cancel them.
        self.identity = DEVICE_IDENTITY # mandatory string setting device identity
        self.connection_type = CONNECTION_TYPE # mandatory string setting device output interface type
        self.sensors = DEVICE_SENSORS # mandatory string indicating the magnitudes measured by the device
        self.addresses = I2C_ADDRESSES # mandatory list indicating the possible addresses where it is possible to find your device on the i2c bus
        self.device_address = 0x00 # default temporary address of your device
        ### here below you can put other variables specific for the operation of your device
        """ for example:
        self.bus = None
        """
        #################################################


### mandatory functions. Do not modify or cancel them.
    def getConnectionType(self):
        return self.connection_type

    def getConnectionParams(self):
        return self.addresses

    def getIdentity(self):
        return self.identity

    def setIdentity(self,idstring):
        self.identity = idstring
        
    def getSensors(self):
        return self.sensors

    def terminate(self):
        self.device_address = 0x00
#########################################################
    

## the mandatory function "connect" check if your device is plugged into the I2C port.
## It returns 1 if your device is found, 0 if it is not found.
## The mandatory argument to pass to the function is the address (which is an integer hexadecimal value)
## where the function is going to search your device

    def connect(self,address):
        found = 0
        try:
            ### put here the code specific for your device
            """
            for example:
            self.bus = SMBus(1)
            data = self.bus.read_i2c_block_data(address,offset,lenght)
            etc...
            """
            ###############################
            self.device_address = address ## if your device is found at the passed address, the device address is set.
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
