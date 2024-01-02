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

import time
from smbus2 import SMBus

CONNECTION_TYPE = "i2c"
I2C_ADDRESSES = [0x68,0x69,0x6A,0x6B,0x6C,0x6D,0x6E,0x6F]
DEVICE_IDENTITY = "MCP342x"
DEVICE_SENSORS = "v1[v];v2[v];v3[v];v4[v]"

class Mcp342x:

    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.connection_type = CONNECTION_TYPE
        self.sensors = DEVICE_SENSORS 
        self.addresses = I2C_ADDRESSES
        self.device_address = 0x00
        self.adc_conf = 0x9C
        self.bus = None
        self.__signbit = 0 # stores the sign bit for the sampled value
        self.__bitrate = 18
        self.__lsb = 0.0000078125
        self.__pga = float(0.5) # current pga setting
        self.__conversionmode = 0  # Conversion Mode


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
## then returns 1 if any mcp342x is found
    def connect(self,address):
        found = 0
        try:
            self.bus = SMBus(1) 
            self.adc_conf = self.__updatebyte(self.adc_conf, 0xF3, 0x0C)
            self.bus.write_byte(address, self.adc_conf)
            self.device_address = address
            found = 1
        except Exception as e:
            pass
        return found


    def sample(self):
        measures = ""
        try:
            for chan in range(1,5,1):
                volt = self.__read_voltage(self.device_address, chan)
                vstr = '{:1.6f}'.format(volt)
                measures = measures + vstr + ";"
            return measures.rstrip(";")
        except Exception as e:
            return ""

    def __updatebyte(self, byte, mask, value):
        """
        Internal method for setting the value of a single bit within a byte
        :param byte: input value
        :type byte: int
        :param mask: location to update
        :type mask: int
        :param value: new bit, 0 or 1
        :type value: int
        :return: updated value
        :rtype: int
        """
        byte &= mask
        byte |= value
        return byte


    def __read_raw(self,address,channel):
        """
        Internal method for reading the raw value from the selected ADC channel
        :param channel: 1 to 8
        :type channel: int
        :raises ValueError: read_raw: channel out of range
        :raises TimeoutError: read_raw: channel x conversion timed out
        :return: raw ADC output
        :rtype: int
        """
        high = 0
        low = 0
        mid = 0
        cmdbyte = 0
        # get the config and i2c address for the selected channel
        self.__setchannel(channel)        
        config = self.adc_conf

        # if the conversion mode is set to one-shot update the ready bit to 1
        if self.__conversionmode == 0:
            config = config | (1 << 7)
            self.bus.write_byte(address, config)
            config = config & ~(1 << 7)  # reset the ready bit to 0

        # determine a reasonable amount of time to wait for a conversion
        seconds_per_sample = 0.26666
        timeout_time = time.time() + (100 * seconds_per_sample)

        # keep reading the adc data until the conversion result is ready
        while True:
            __adcreading = self.bus.read_i2c_block_data(address, config, 4)
            high = __adcreading[0]
            mid = __adcreading[1]
            low = __adcreading[2]
            cmdbyte = __adcreading[3]
            # check if bit 7 of the command byte is 0.
            if(cmdbyte & (1 << 7)) == 0:
                break
            elif time.time() > timeout_time:
                msg = 'read_raw: channel %i conversion timed out' % channel
                raise TimeoutError(msg)
            else:
                time.sleep(0.00001)  # sleep for 10 microseconds
        self.__signbit = False
        raw = 0
        # extract the returned bytes and combine in the correct order
        raw = ((high & 0x03) << 16) | (mid << 8) | low
        self.__signbit = bool(raw & (1 << 17))
        raw = raw & ~(1 << 17)  # reset sign bit to 0
        return raw


    def __setchannel(self, channel):
        """
        Internal method for updating the config to the selected channel
        :param channel: selected channel
        :type channel: int
        """
        if channel == 1:  # bit 5 = 1, bit 6 = 0
            self.adc_conf = self.__updatebyte(self.adc_conf,0x9F, 0x00)
        elif channel == 2:  # bit 5 = 1, bit 6 = 0
            self.adc_conf = self.__updatebyte(self.adc_conf,0x9F, 0x20)
        elif channel == 3:  # bit 5 = 0, bit 6 = 1
            self.adc_conf = self.__updatebyte(self.adc_conf,0x9F, 0x40)
        elif channel == 4:  # bit 5 = 1, bit 6 = 1
            self.adc_conf = self.__updatebyte(self.adc_conf,0x9F, 0x60)
        return


    def __read_voltage(self, address, channel):
        """
        Internal method for returning the voltage from the selected ADC channel
        :param channel: 1 to 8
        :type channel: int
        :return: voltage
        :rtype: float
        """
        raw = self.__read_raw(address,channel)
        voltage = float(0.0)
        if not self.__signbit:
            voltage = float(
                (raw * (self.__lsb / self.__pga)) * 2.471)
        return voltage


    def set_conversion_mode(self, mode):
        """
        conversion mode for adc

        :param mode: 0 = One shot conversion mode
                     1 = Continuous conversion mode
        :type mode: int
        :raises ValueError: set_conversion_mode: mode out of range
        """
        if mode == 0:
            # bit 4 = 0
            self.adc_conf = self.__updatebyte(self.adc_conf, 0xEF, 0x00)
            self.__conversionmode = 0
        elif mode == 1:
            # bit 4 = 1
            self.adc_conf = self.__updatebyte(self.adc_conf, 0xEF, 0x10)
            self.__conversionmode = 1
        else:
            raise ValueError('set_conversion_mode: mode out of range')
        return
