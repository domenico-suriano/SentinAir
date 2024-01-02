# -*- coding: cp1252 -*-
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

from ctypes import c_short
import time

CONNECTION_TYPE = "i2c" # mandatory string which indicates that the device is interfaced by a I2C bus. Do not modify this one.
# mandatory list which indicates the possible i2c bus addresses where your device must be searched.
# You can modify it by inserting the values right for your device operation
# following the example below
# I2C_ADDRESSES = [0x68,0x69,0x6A,0x6B,0x6C,0x6D,0x6E,0x6F]
I2C_ADDRESSES = [0x76,0x77]
#############################################################################

DEVICE_IDENTITY = "bme280" # mandatory string indicating the device name. Modify it with your device name.

# mandatory string indicating the magnitudes measured by the device. It must have fields separated by ";"
# as in the example below
# DEVICE_SENSORS = "V1[V];V2[V];V3[V];V4[V]". Modify it for your device operation.
DEVICE_SENSORS = "t[c];p[hPa];rh[%]"
###################################

#### Here below you can put other constants specific for the operation of your device
# BME280 microprocessor Register Addresses
REG_DATA = 0xF7
REG_CONTROL = 0xF4
REG_CONFIG  = 0xF5
REG_CONTROL_HUM = 0xF2
REG_HUM_MSB = 0xFD
REG_HUM_LSB = 0xFE
REG_ID = 0xD0 #Chip ID Register Address
# chip working mode
MODE = 1
# Oversample settings - see page 27 of bme280 datasheet
OVERSAMPLE_TEMP = 2
OVERSAMPLE_PRES = 7 # means oversampling = 16x 
OVERSAMPLE_HUM = 2
IIR_FILTER = 7 # means iir filter setting = 16x
###############################################


class Bme280: #it is mandatory that the class name must have the same name of the file (i2c-device-template.py) with the capital first letter

    def __init__(self):
        ### mandatory variables. Do not modify or cancel them.
        self.identity = DEVICE_IDENTITY # mandatory string setting device identity
        self.connection_type = CONNECTION_TYPE # mandatory string setting device output interface type
        self.sensors = DEVICE_SENSORS # mandatory string indicating the magnitudes measured by the device
        self.addresses = I2C_ADDRESSES # mandatory list indicating the possible addresses where it is possible to find your device on the i2c bus
        self.device_address = 0x00 # default temporary address of your device
        ### here below you can put other variables specific for the operation of your device
        self.bus = None
        self.chip_id = 0
        self.cal1 = None
        self.cal2 = None
        self.cal3 = None
        self.dig_T1 = None
        self.dig_T2 = None
        self.dig_T3 = None
        self.dig_P1 = None
        self.dig_P2 = None
        self.dig_P3 = None
        self.dig_P4 = None
        self.dig_P5 = None
        self.dig_P6 = None
        self.dig_P7 = None
        self.dig_P8 = None
        self.dig_P9 = None
        self.dig_H1 = None
        self.dig_H2 = None
        self.dig_H3 = None
        self.dig_H4 = None
        self.dig_H5 = None
        self.dig_H6 = None
        self.iir_setting = IIR_FILTER << 2
        self.control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
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
            self.bus = SMBus(1)
            data = self.bus.read_i2c_block_data(address,REG_ID,2)
            self.chip_id = data[0]
            self.bus.write_byte_data(address, REG_CONTROL_HUM, OVERSAMPLE_HUM)
            self.bus.write_byte_data(address, REG_CONFIG, self.iir_setting)
            # Read blocks of calibration data from EEPROM
            # See Page 24 data sheet
            self.cal1 = self.bus.read_i2c_block_data(address, 0x88, 24)
            self.cal2 = self.bus.read_i2c_block_data(address, 0xA1, 1)
            self.cal3 = self.bus.read_i2c_block_data(address, 0xE1, 7)
            # return two bytes from data as an unsigned 16-bit value
            self.dig_T1 =(self.cal1[1] << 8) + self.cal1[0]
            # return two bytes from data as a signed 16-bit value
            self.dig_T2 = c_short((self.cal1[3] << 8) + self.cal1[2]).value
            self.dig_T3 = c_short((self.cal1[5] << 8) + self.cal1[4]).value
            self.dig_P1 = (self.cal1[7] << 8) + self.cal1[6] # return two bytes from data as an unsigned 16-bit value
            self.dig_P2 = c_short((self.cal1[9] << 8) + self.cal1[8]).value
            self.dig_P3 = c_short((self.cal1[11] << 8) + self.cal1[10]).value
            self.dig_P4 = c_short((self.cal1[13] << 8) + self.cal1[12]).value
            self.dig_P5 = c_short((self.cal1[15] << 8) + self.cal1[14]).value
            self.dig_P6 = c_short((self.cal1[17] << 8) + self.cal1[16]).value
            self.dig_P7 = c_short((self.cal1[19] << 8) + self.cal1[18]).value
            self.dig_P8 = c_short((self.cal1[21] << 8) + self.cal1[20]).value
            self.dig_P9 = c_short((self.cal1[23] << 8) + self.cal1[22]).value
            self.dig_H1 = self.cal2[0] & 0xFF # return one byte from data as an unsigned char
            self.dig_H2 = c_short((self.cal3[1] << 8) + self.cal3[0]).value
            self.dig_H3 = self.cal3[2] & 0xFF
            # return one byte from data as a signed char
            _dig_H4 = self.cal3[3]
            if _dig_H4 > 127:
                _dig_H4 -= 256
            _dig_H4 = (_dig_H4 << 24) >> 20
            if self.cal3[4] > 127:
                char_cal3 -= 256
            else:
                char_cal3 = self.cal3[4]
            self.dig_H4 = _dig_H4 | (char_cal3 & 0x0F)
            _dig_H5 = self.cal3[5]
            if _dig_H5 > 127:
                _dig_H5 -= 256
            _dig_H5 = (_dig_H5 << 24) >> 20
            uchar_cal3 = self.cal3[4] & 0xFF
            self.dig_H5 = _dig_H5 | (uchar_cal3 >> 4 & 0x0F)
            _dig_H6 = self.cal3[6]
            if _dig_H6 > 127:
                _dig_H6 -= 256            
            self.dig_H6 = _dig_H6
            ###############################
            self.device_address = address ## if your device is found at the passed address, the device address is set.
            found = 1
        except Exception as e:
            self.bus = None
        return found


## the mandatory function sample returns the reading of the magnitudes measured by your device.
## It is mandatory that the measures returned are in a string having fields separated by ";". For example: "2.12;4.32;1.21;0.34"
## The number of fields must be the same of the DEVICE_SENSORS constant. If you have just one field,
## the returned string will be,for example, "2.12"

    def sample(self):
        measures = ""
        try:
            ### put here the code specific for your device
            self.bus.write_byte_data(self.device_address, REG_CONTROL, self.control)
            time.sleep(0.2)
            data_in = self.bus.read_i2c_block_data(self.device_address, REG_DATA, 8)
            t = self.__read_temperature(data_in)
            p = self.__read_pressure(data_in,t)
            h = self.__read_humidity(data_in,t)
            measures = '{:3.2f}'.format(t) + ";" + '{:4.3f}'.format(p) + ";" + '{:3.2f}'.format(h)
            ###############################
            return measures.rstrip(";")
        except Exception as e:
            return ""

## Here below you can put other functions specific for your device operation
    def chip_identity(self):
        return self.chip_id

    def __read_temperature(self,data):
        raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        var1 = ((((raw>>3)-(self.dig_T1<<1)))*(self.dig_T2)) >> 11
        var2 = (((((raw>>4) - (self.dig_T1)) * ((raw>>4) - (self.dig_T1))) >> 12) * (self.dig_T3)) >> 14
        t = var1+var2
        return float(((t * 5) + 128) >> 8)/100.0;

    def __read_pressure(self,data,temp):
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        var1 = temp / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0
        var2 = var2 + var1 * self.dig_P5 * 2.0
        var2 = var2 / 4.0 + self.dig_P4 * 65536.0
        var1 = (self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_P1
        if var1 == 0:
            pressure=0
        else:
            pressure = 1048576.0 - pres_raw
            pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
            var1 = self.dig_P9 * pressure * pressure / 2147483648.0
            var2 = pressure * self.dig_P8 / 32768.0
            pressure = pressure + (var1 + var2 + self.dig_P7) / 16.0
        return pressure/100.0;

    def __read_humidity(self,data,temp):
        hum_raw = (data[6] << 8) | data[7]
        humidity = temp - 76800.0
        humidity = (hum_raw - (self.dig_H4 * 64.0 + self.dig_H5 / 16384.0 * humidity)) * (self.dig_H2 / 65536.0 * (1.0 + self.dig_H6 / 67108864.0 * humidity * (1.0 + self.dig_H3 / 67108864.0 * humidity)))
        humidity = humidity * (1.0 - self.dig_H1 * humidity / 524288.0)
        if humidity > 100:
            humidity = 100
        elif humidity < 0:
            humidity = 0
        return humidity
###################################################
