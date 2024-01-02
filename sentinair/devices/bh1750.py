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

from smbus2 import SMBus
import time
 
# Define some constants from the datasheet
CONNECTION_TYPE = "i2c"
I2C_ADDRESSES = [0x23,0x5C] # Default device I2C address 0x23
DEVICE_IDENTITY = "BH1750"
DEVICE_SENSORS = "l[lux]"
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20




class Bh1750:
    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.addresses = I2C_ADDRESSES
        self.connection_type = CONNECTION_TYPE
        self.sensors = DEVICE_SENSORS
        self.address = 0x00
        self.bus = None
    

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


## the function "connect" check if the device is plugged into the I2C port,
## then returns 1 if any bh1750 is found
    def connect(self,address):
        found = 0
        try:
            self.bus = SMBus(1)
            data = self.bus.read_i2c_block_data(address,ONE_TIME_HIGH_RES_MODE,2)
            meas = '{:5.1f}'.format(self.__convertToNumber(data))
            self.address = address
            found = 1
        except Exception as e:
            pass
        return found


    def __convertToNumber(self,data):
        # Simple function to convert 2 bytes of data
        # into a decimal number
        try:
            return float((data[1] + (256 * data[0])) / 1.2)
        except Exception as e:
            return -1.0


    def sample(self):
        try:
            data = self.bus.read_i2c_block_data(self.address,ONE_TIME_HIGH_RES_MODE,2)
            meas = '{:5.1f}'.format(self.__convertToNumber(data))
            return meas.lstrip(" ")
        except Exception as e:
            return ""
