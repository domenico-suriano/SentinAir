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

import serial
import time
import struct

DEVICE_IDENTITY = "SPS30"
CONNECTION_TYPE = "serial"
DEVICE_BAUD_RATE = 115200
DEVICE_SENSORS = "pm1[ug/m3];pm2.5[ug/m3];pm4[ug/m3];pm10[ug/m3]"

SERIAL_NUMBER = "00080000"
SERIAL_TIMEOUT = 3
ERR_STR = "-100.0;-100.0;-100.0;-100.0"
ERR_STR1 = "-10.0;-10.0;-10.0;-10.0"
ERR_STR2 = "-20.0;-20.0;-20.0;-20.0"
ERR_STR3 = "-30.0;-30.0;-30.0;-30.0"
ERR_STR4 = "-40.0;-40.0;-40.0;-40.0"


class Sps30:

    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.connection_type = CONNECTION_TYPE
        self.sensors = DEVICE_SENSORS
        self.baud_rate = DEVICE_BAUD_RATE
        self.portname = ""
        self.port = None
        self.strmeas = "0.0;0.0;0.0;0.0"

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
    
    
    def __CRCcheck(self,inp):
        crc = 0
        inp1 = list(inp[1:-2])
        try:
            for i in inp1:
                crc = crc + i
            crcb = crc.to_bytes(2,'big')
            chk = 255 - crcb[1]
            if chk == inp[-2]:
                  return 1
            return 0
        except Exception as e:
            return 0


## the function "connect" check if the device is plugged into serport,
## then returns 1 if the device is found
    def connect(self,serport):
        found = 0
        try:
            self.port = serial.Serial(serport,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
            r = self.port.write(b"\x7E\x00\xD0\x01\x00\x2E\x7E")
            read = self.port.read(16)
            serialn = list(read[5:13])
            sn = ''.join(chr(e) for e in serialn)
            if self.__CRCcheck(read) == 1:
                if sn == SERIAL_NUMBER:
                    return 1
                else:
                    return found
            return 0
        except Exception as e:
            return found



    def sample(self):
        try:
            r = self.port.write(b"\x7E\x00\x00\x02\x01\x03\xF9\x7E")
            read = self.port.read(7)
            if self.__CRCcheck(read) == 0:
                return ERR_STR1
            time.sleep(1.1)
            self.port.flushInput()
            r = self.port.write(b"\x7E\x00\x03\x00\xFC\x7E")
            time.sleep(0.1)
            nb = self.port.inWaiting()
            nread = 0
            while nb <= 1 and nread < 2:
                nb = self.port.inWaiting()
                nread = nread + 1
            indata = self.port.read(nb)
            nread = 0
            while indata[-1] == b'0x7E' and nread < 2:
                nb = self.port.inWaiting()
                indata = self.port.read(nb)
                nread = nread + 1
                time.sleep(0.2)
            # byte stuffing removing
            if b'\x7D\x5E' in indata:
                indata = indata.replace(b'\x7D\x5E', b'\x7E')
            if b'\x7D\x5D' in indata:
                indata = indata.replace(b'\x7D\x5D', b'\x7D')
            if b'\x7D\x31' in indata:
                indata = indata.replace(b'\x7D\x31', b'\x11')
            if b'\x7D\x33' in indata:
                indata = indata.replace(b'\x7D\x33', b'\x13')
            if self.__CRCcheck(indata) == 0:
                return ERR_STR2
            data = indata[5:-2]
            try:
                meas1 = struct.unpack(">ffffffffff", data)
                meas2 = meas1[:4]
            except struct.error:
                return ERR_STR3
            time.sleep(0.1)
            self.port.flushInput()
            r = self.port.write(b"\x7E\x00\x01\x00\xFE\x7E")
            read = self.port.read(7)
            meas = '{:.1f}'.format(meas2[0]) + ";" + '{:.1f}'.format(meas2[1]) + ";" + '{:.1f}'.format(meas2[2]) + ";" + '{:.1f}'.format(meas2[3])
        except Exception as e:
            return ERR_STR4
        return meas
    
