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

### WARNING: PMS3003_BAUD_RATE depends on the settings
### of your Plantower device PMS3003, therefore check on them and
### update or modify them if necessary.

import serial
import _thread
import time

DEVICE_IDENTITY = "PMS3003"
CONNECTION_TYPE = "serial"
DEVICE_BAUD_RATE = 9600
DEVICE_SENSORS = "pm1[ug/m3];pm2.5[ug/m3];pm10[ug/m3]"

SERIAL_TIMEOUT = 2
MAX_NUM_ATTEMPT = 10
ERR_VAL = "-100"

class Pms3003:

    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.connection_type = CONNECTION_TYPE
        self.sensors = DEVICE_SENSORS
        self.baud_rate = DEVICE_BAUD_RATE
        self.portname = ""
        self.port = None
        self.lesteningthread = 0
        self.strmeas = "0.0;0.0;0.0"

    def getSensors(self):
        return self.sensors

    def getIdentity(self):
        return self.identity

    def setIdentity(self,idstring):
        self.identity = idstring

    def getConnectionType(self):
        return self.connection_type

    def getConnectionParams(self):
        return [self.portname,self.baud_rate]

    def terminate(self):
        self.lesteningthread = 0
        try:
            self.port.close()
        except:
            return

    def __del__(self):
        self.lesteningthread = 0
        try:
            self.port.close()
        except:
            return

## the function "connect" check if the device is plugged into serport,
## then returns 1 if the device is found
    def connect(self,serport):
        found = 0
        if (serport.find("ttyACM")>= 0):
            return found
        try:
            self.port = serial.Serial(serport,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
        except Exception as e:
            return found
        num_attempt = 0
        while num_attempt < MAX_NUM_ATTEMPT:
            try:
                time.sleep(0.3)
                buf = self.port.read(24)
                if (buf[0] == 66) and (buf[1] == 77):
                    val1_0 = float(buf[10]*256 + buf[11])
                    val2_5 = float(buf[12]*256 + buf[13])
                    val10 = float(buf[14]*256 + buf[15])
                    strmeas = str(val1_0) + ";" + str(val2_5) + ";" + str(val10)
                    self.lesteningthread = 1
                    ser = serport.split("/")
                    ser1 = ser[-1]
                    _thread.start_new_thread(self.__capture,())
                    self.portname = serport
                    found = 1
                    return found
                if len(buf) == 0:
                    num_attempt = num_attempt + 1
                if (buf[0] != 66) or (buf[1] != 77):
                    num_attempt = num_attempt + 1
                    self.port.close()
                    time.sleep(1)
                    self.port.open()
            except Exception as e:
                num_attempt = num_attempt + 1
        return found

## the function "sample" reads the sensor output,
## then returns a string separate by semicolon containing data
## if an error happens, it returns the string with err value: "-100.0"
    def sample(self):
        return self.strmeas

    def __capture(self):
        while self.lesteningthread:
            try:
                buf = self.port.read(24)
                if (buf[0] == 66) and (buf[1] == 77):
                    try:
                        val1_0 = float(buf[10]*256 + buf[11])
                        val2_5 = float(buf[12]*256 + buf[13])
                        val10 = float(buf[14]*256 + buf[15])
                        self.strmeas = str(val1_0) + ";" + str(val2_5) + ";" + str(val10)
                    except Exception as e:
                        time.sleep(0.1)
                if len(buf) == 0:
                    self.strmeas = ERR_VAL + ";" + ERR_VAL + ";" + ERR_VAL
                if (buf[0] != 66) or (buf[1] != 77):
                    self.strmeas = ERR_VAL + ";" + ERR_VAL + ";" + ERR_VAL
            except Exception as e:
                self.strmeas = ERR_VAL + ";" + ERR_VAL + ";" + ERR_VAL
