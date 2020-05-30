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

import serial
import time

IRCA1_DEVICE_TYPE = "IRC-A1"
IRCA1_CONNECTION_TYPE = "usb"
IRCA1_BAUD_RATE = 19200
SERIAL_TIMEOUT = 2
MAX_NUM_ATTEMPT = 4
ERR_VAL = "-100"

class Irca1:

    def __init__(self):
        self.device_type = IRCA1_DEVICE_TYPE
        self.identity = ""
        self.connection_type = IRCA1_CONNECTION_TYPE
        self.baud_rate = IRCA1_BAUD_RATE
        self.sensors = "co2[ppm]"
        self.port = None
        self.portname = ""

## the function "connect" check if the device is plugged into serport,
## then returns 1 if irca1 is found
    def connect(self,serport):
        if (serport.find("ttyACM") >= 0):
            return 0
        if (serport.find("ttyAMA") >= 0):
            return 0
        try:
            self.port = serial.Serial(serport,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
        except:
            return 0
        num_attempt = 0
        while num_attempt < MAX_NUM_ATTEMPT:
            try:
                time.sleep (0.2)
                self.port.write("N\r".encode('utf-8'))
                res =  self.port.readline().decode()
                time.sleep(0.1)
                res2 = res.rstrip("\r\n")
                res3 = float(res2)
                srp = serport.split("/")
                srp1 = srp[-1]
                self.identity = "IRCA1-" + srp1
                self.portname = serport
                return 1
            except:
                num_attempt = num_attempt + 1
        return 0
    
    def getConnectionParams(self):
        return [self.portname,self.baud_rate]

    def getConnectionType(self):
        return self.connection_type

    def getIdentity(self):
        return self.identity

    def getSensors(self):
        return self.sensors

    def getDeviceType(self):
        return self.device_type

## the function "sample" reads the sensor output,
## then returns a string separate by semicolon containing data
## if an error happens, it returns the string with err value: "-100.0"
    def sample(self):
        try:
            ans = ""
            self.port.write("N\r".encode('utf-8'))
            buf1 = self.port.readline().decode()
            buf3 = buf1.rstrip("\r\n")
            buf4 = buf3.lstrip(' ')
            if buf4 == "":
                return ERR_VAL
            return buf4
        except Exception as e:
            return ERR_VAL


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

