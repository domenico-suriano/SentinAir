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

DEVICE_IDENTITY = "LCSS_ADAPTER"
CONNECTION_TYPE = "usb"
DEVICE_BAUD_RATE = 115200
DEVICE_SENSORS = "S1[V];S2[V];S3[V];S4[V];S5[V];S6[V];S7[V];S8[V];T[C];RH[%];pwr[V]"

SERIAL_TIMEOUT = 2
MAX_NUM_ATTEMPT = 4
ERR_VAL = "-100"

class Lcss_adapter:

    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.connection_type = CONNECTION_TYPE
        self.baud_rate = DEVICE_BAUD_RATE
        self.sensors = DEVICE_SENSORS
        self.port = None
        self.portname = ""
        
    def getConnectionType(self):
        return self.connection_type

    def getIdentity(self):
        return self.identity

    def setIdentity(self,idstring):
        self.identity = idstring
        
    def getSensors(self):
        return self.sensors

    def getConnectionParams(self):
        return [self.portname,self.baud_rate]

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


## the function "connect" check if the device is plugged into serport,
## then returns 1 if the device is found
    def connect(self,serport):
        found = 0
        if (serport.find("ttyACM") >= 0):
            return found
        if (serport.find("ttyAMA") >= 0):
            return found
        try:
            self.port = serial.Serial(serport,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
        except Exception as e:
            return found
        try:
            num_attempt = 0
            while num_attempt < MAX_NUM_ATTEMPT:
                time.sleep (0.1)
                self.port.write('i'.encode('utf-8'))
                idstr = self.port.readline().decode()
                if idstr[0:5] == "NASUS":
                    self.identity = idstr.rstrip("\r\n")
                    time.sleep (0.1)
                    self.port.write('h'.encode('utf-8'))
                    self.sensors = self.port.readline().decode().rstrip("\r\n")
                    self.portname = serport
                    srp = serport.split("/")
                    srp1 = srp[-1]
                    found = 1
                    return found
                elif idstr == "":
                    num_attempt = num_attempt + 1
                    continue
                else:
                    self.port.close()
                    time.sleep(0.2)
                    break
            self.port.close()
            return found        
        except Exception as e:
            self.port.close()
            return found

## the function "sample" reads the sensor output,
## then returns a string separate by semicolon containing data
## if an error happens, it returns the string with err value: "-100.0"
    def sample(self):
        try:
            ans = ""
            self.port.write('g'.encode('utf-8'))
            buf1 = self.port.readline().decode()
            buf2 = buf1.replace('\r','')
            ans = ans + buf2.replace('\n','')
            if ans == "":
                mis = self.sensors.split(';')
                reterr = ""
                for mm in mis:
                    reterr = reterr + ERR_VAL + ";"
                ans = reterr.rstrip(";")
            return ans
        except Exception as e1:
            mis = self.sensors.split(';')
            reterr = ""
            for mm in mis:
                reterr = reterr + ERR_VAL + ";"
            ans = reterr.rstrip(";")            
            return ans
