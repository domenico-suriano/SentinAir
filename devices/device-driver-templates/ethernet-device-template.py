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
import socket # mandatory library to import
################################


#############In this section the necessary constants should be placed. Here below it is an example
CONNECTION_TYPE = "eth" # mandatory string which indicates that the device is interfaced by the Ethernet socket. Do not modify this one.

# mandatory list which indicates the possible addresses where your device must be searched.
# You can modify it by inserting the values right for your device operation
# following the example below
# ETH_ADDRESSES = ["192.168.20.43","192.168.20.44"]
ETH_ADDRESSES = ["address1","address2"]
######################################################################################################

DEVICE_IDENTITY = "device name chosen by the user" # mandatory string indicating the device name. Modify it with your device name.

# mandatory string indicating the magnitudes measured by the device. It must have fields separated by ";"
# as in the example below
# DEVICE_SENSORS = "NO2[ppb];NO[ppb];NOx[ppb]". Modify it for your device operation.
"""
if you have just one field, then the constant will be:
DEVICE_SENSORS = "NO2[ppb]"
"""
DEVICE_SENSORS = "field1[unit of measure 1];field2[unit of measure 2];field3[unit of measure 3]"
###################################

#### Here below you can put other constants specific for the operation of your device
""" for example:
SOCKET_TIMEOUT = 2
"""
###############################################


class Ethernet-device-template: #it is mandatory that the class name must have the same name of the file (ethernet-device-template.py) with the capital first letter

    def __init__(self):
        ### mandatory variables. Do not modify or cancel them.
        self.identity = DEVICE_IDENTITY # mandatory string setting device identity
        self.connection_type = CONNECTION_TYPE # mandatory string setting device output interface type
        self.sensors = DEVICE_SENSORS # mandatory string indicating the magnitudes measured by the device
        self.addresses = ETH_ADDRESSES # mandatory list indicating the possible addresses where it is possible to find your device on the net
        self.device_address = None # mandatory variable where it is going to be stored your device address
        self.sk = None # mandatory variable which is going to store the socket object from the "socket" library
        ### here below you can put other variables specific for the operation of your device
        """ for example:
        self.port = 8000
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
        try:
            self.sk.close()
        except:
            return

    def __del__(self):
        try:
            self.sk.close()
        except:
            return
#########################################################
    

## the mandatory function "connect" check if your device is conected to the net set up by SentinAir.
## It returns 1 if your device is found, 0 if it is not found.
## The mandatory argument to pass to the function is the address (which is a string: e.g: "192.168.20.43")
## where the function is going to search your device
    def connect(self,address):
        found = 0
        try:
            ### put here the code specific for your device
            """
            for example:
            self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sk.settimeout(SOCKET_TIMEOUT)
            data_sent = self.sk.sendto(command.encode(), (address,self.port))
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
