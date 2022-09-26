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

### WARNING: PMS5003_BAUD_RATE depends on the settings
### of your Plantower device PMS5003, therefore check on them and
### update or modify them if necessary.

import serial
import time

DEVICE_IDENTITY = "PMS5003"
CONNECTION_TYPE = "serial"
DEVICE_BAUD_RATE = 9600
DEVICE_SENSORS = "pm1[ug/m3];pm2.5[ug/m3];pm10[ug/m3]"

SERIAL_TIMEOUT = 2
MAX_NUM_ATTEMPT = 10
ERR_VAL = "-100"

class Pms5003:

    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.connection_type = CONNECTION_TYPE
        self.sensors = DEVICE_SENSORS
        self.baud_rate = DEVICE_BAUD_RATE
        self.portname = ""
        self.port = None
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
                self.port.write([66, 77, 225, 0, 0, 1, 112])
                buf = self.port.read(8)
                if (buf[0] == 66) and (buf[1] == 77):
                    ck = 0
                    for a in range(5):
                       ck = ck + buf[a]
                    ck = ck & 255
                    if ck == buf[7]:
                        self.portname = serport
                        found = 1
                        return found
                if len(buf) == 0:
                    num_attempt = num_attempt + 1
                    continue
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
        num_attempt = 0
        self.strmeas = ERR_VAL + ";" + ERR_VAL + ";" + ERR_VAL
        while num_attempt < MAX_NUM_ATTEMPT:
            try:
                time.sleep(0.4)
                self.port.write([66, 77, 226, 0, 0, 1, 113])
                buf = self.port.read(32)
                if (buf[0] == 66) and (buf[1] == 77):
                    cs = (buf[30] * 256 + buf[31])
                    check = 0
                    for i in range(30):
                        check += buf[i]
                    if check != cs:
                        num_attempt = num_attempt + 1
                        continue
                    pm1 = float(buf[10] * 256 + buf[11])
                    pm25 = float(buf[12] * 256 + buf[13])
                    pm10 = float(buf[14] * 256 + buf[15])
                    self.strmeas = str(pm1) + ";" + str(pm25) + ";" + str(pm10)
                    return self.strmeas
            except Exception as e:
                num_attempt = num_attempt + 1
        return self.strmeas
