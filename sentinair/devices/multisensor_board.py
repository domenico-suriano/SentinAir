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
import libscrc
import struct
import time
from collections import deque


CONNECTION_TYPE = "usb"
DEVICE_IDENTITY = "MULTISENSOR"
DEVICE_SENSORS = ""
DEVICE_BAUD_RATE = 115200

SERIAL_TIMEOUT = 2
MAX_NUM_ATTEMPT = 10

ERR_VAL = "-100"

#define the max number of time that I send the message if the multisensor answer wrong
MAX_ITERATION=4

#the multisensor max lenght buffer size
MAX_MODBUS_BYTES=200

#LIST of modbus function
MODBUS_READ_SINGLE_REGISTER = 3
MODBUS_WRITE_SINGLE_REGISTER = 6
MODBUS_STATE_REGISTER_MEASURE_CYCLE = 0x07
MODBUS_STATE_REGISTER_REBOOT = 0x0A
MODBUS_STATE_REGISTER_SERIAL_NUMBER = 0x01
MODBUS_STATE_REGISTER_MEASURE_CYCLE = 0x07
MODBUS_DATA_READ_MEASURES = 0x19
MODBUS_STATE_REGISTER_SCAN_AFE = 0x08
MODBUS_STATE_REGISTER_READY = 0x02
MODBUS_DATA_MEASURE_NAMES = 0x15
MODBUS_DATA_NUMBER_OF_MEASURE = 0x14

#set the MODBUS address of the board, it is configured using the dip switch on the board
multisensor_address = 0x2


def get_multisensor_address():
    return multisensor_address


#************basic_check*************
#input: data_in: bytes read from the serial port
#       multisensor_address: address of the multisensor
#       modbus_function: function of the request
#output: data_in (bytearray). 1 byte 0 for error, read bytes if ok
#************************************
def basic_check(data_in, address, modbus_function):
    data_len=len(data_in)
    #basic check on data lenght: if the read_data is zero lenght it is an error. Return 0
    if data_len==0:
        #return 0 as error flag
        return bytes([0])   
    #consider the last two bytes as the incoming CRC information (calculated by the uC)
    crc_in=bytes([data_in[data_len-2],data_in[data_len-1]])
    #format into an unsigned integer number
    [crc_in]=struct.unpack('>H', crc_in)
    #calculate the CRC of the received data
    crc_calc=libscrc.modbus(data_in[0:data_len-2])
    #if the CRC is not correct generate an error
    if (crc_in!=crc_calc):
        #return 0 as error flag
        return bytes([0])
    #now check that the multisensor address and function echoed by the mulstisensor match the reqeusted one
    if data_in[0]!=address or data_in[1]!=modbus_function:
        return bytes([0])
    #the basic check was ok. Return data
    return data_in


#************read_REBOOT**************************************************** 
#description: sends a command to reboot the system
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#output: none
#***************************************************************************  
def read_REBOOT(ser, address):
    #check if the serial port is open
    if ser.is_open==False:
        return 0
    #reset the output buffer before send new data    
    ser.reset_output_buffer   
    out=[address, MODBUS_READ_SINGLE_REGISTER, 0x0, MODBUS_STATE_REGISTER_REBOOT, 0, 0]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))          
    write_message(system,ser,out,address)
    time.sleep(5)       
    #close the serial port to be sure it can be used again after sending the reboot command
    ser.close()
    #add a delay to be sure the port has been closed
    time.sleep(2)
    #re-open serial port
    ser.open()
    #add a delay to be sure the port has been opened
    time.sleep(2)          
    return


#************write_message************
#input: serial porta, buffer to write
#output: none
#************************************
def write_message(ser,msg,multisensor_address):
    try:     
        ser.write(msg)
    except:
        time.sleep(2)
        #first try to close, open and reboot the system
        try:
            ser.close()
            time.sleep(2)
            ser.open()
            read_REBOOT( ser, multisensor_address)
        #if i fail to close the port (already closed) i open it and reboot            
        except:
            ser.open()
            #reboot the system
            read_REBOOT( ser, multisensor_address)


#************read_message************
#input: system, multisensor modbus address, modbus function,serial port
#output: read_data (bytearray)
#************************************
def read_message (multisensor_address, modbus_function, ser):
    try:
        read_data = ser.read(MAX_MODBUS_BYTES)
        return basic_check(read_data, multisensor_address, modbus_function)
    #if an error occurs during serial operation i go into the except case
    except:
        time.sleep(2)
        #first try to close, open and reboot the system
        try:
            ser.close()
            time.sleep(2)
            ser.open()
            read_REBOOT(ser, multisensor_address)
        #if i fail to close the port (already closed) i open it and reboot
        except:
            ser.open()
            #reboot the system
            read_REBOOT(ser, multisensor_address)




#************error_in_message_check*************
#description: check if the message has the two
#             first data bytes as error (0x0 0x1) 
#             or ok (0x1 0x0) 
#input: data_in: bytes read from the serial port
#output: data_in (bytearray). 1 byte 0 for error, read bytes if ok
#**********************************************
def error_in_message_check(data_in):
    #the message must be at least 7 bytes
    if (len(data_in)<7):
        return bytes([0])
    #the answer includes the special string "0x0 0x1: ERROR"
    if (data_in[4]==0 and data_in[5]==1):
        return bytes([0])
    return data_in


def write_SCAN_AFE(ser, address):
    #check if the serial port is open
    if ser.is_open==False:
        print("write_SCAN_AFE: serial port not open.")
        return bytes ([0])
    #reset the output buffer before send new data
    ser.reset_output_buffer
    #build the modbus message to send
    out=[address, MODBUS_WRITE_SINGLE_REGISTER, 0x0, MODBUS_STATE_REGISTER_SCAN_AFE, 0, 0]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))    
    #send data and read the answer. If any error send the message again before give up.
    j=0;
    while j<MAX_ITERATION:
        write_message(ser,out,address)
        #read the return message
        read_data=read_message(address, MODBUS_WRITE_SINGLE_REGISTER,ser)
        if not(read_data[0]==0 and len(read_data)==1):
            #force loop exit
            j=MAX_ITERATION+1
        else:
            j=j+1
    #if no error return ok
    if (error_in_message_check(read_data)[0]!=0):
        return bytes ([1])
    return bytes ([0])


#************read_READY*********************
#description: read information if the AFE connection has been 
#             verified or not yet
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#output: 4 bytes of the resultin string that contains the multisensor
#       serial number
#*******************************************************************
def read_READY(ser, address):
    #check if the serial port is open
    if ser.is_open==False:
        print("read_READY: serial port not open.")
        return bytes ([0])
    #reset the output buffer before send new data    
    ser.reset_output_buffer
    #build the modbus message to send
    out=[address, MODBUS_READ_SINGLE_REGISTER, 0x0, MODBUS_STATE_REGISTER_READY, 0, 0]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))       
    #send data and read the answer. If any error send the message again before give up.        
    j=0;
    while j<MAX_ITERATION:        
        write_message(ser,out,address)
        #read the return message
        read_data=read_message(address, MODBUS_READ_SINGLE_REGISTER,ser)
        if not(read_data[0]==0 and len(read_data)==1):
            #force loop exit
            j=MAX_ITERATION+1
        else:
            j=j+1         
    if (read_data[0]==0):
        print("read_READY: error in reading data")
        return read_data
    #the string is valid, check the result. if the data bytes are 0x1 0x0 ready is ok
    if (read_data[4]==1 and read_data[5]==0):
        return bytes ([1])
    return bytes ([0])


#************read_SERIAL_NUMBER*************
#description: read the four bytes multisensor serial number
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#output: 4 bytes of the resulting string that contain the multisensor
#       serial number
#*******************************************************************
def read_SERIAL_NUMBER( ser, address):
    #check if the serial port is open
    if ser.is_open==False:
        print("read_SERIAL_NUMBER: serial port not open.")
        return bytes ([0])
    #reset the output buffer before send new data
    ser.reset_output_buffer
    #build the modbus message to send
    out=[address, MODBUS_READ_SINGLE_REGISTER, 0x0, MODBUS_STATE_REGISTER_SERIAL_NUMBER, 0x0, 0x0]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))    
    #send data and read the answer. If any error send the message again before give up.        
    j=0;
    while j<MAX_ITERATION:
        write_message(ser,out,address)
        #read the return message
        read_data=read_message(address, MODBUS_READ_SINGLE_REGISTER,ser)
        #if read data byte 1 is zero that means error
        if not(read_data[0]==0 and len(read_data)==1):
            #information is contained in the following bytes of the valid answer
            data_in_result=read_data[4:8]
            return data_in_result
        else:
            j=j+1
    print("read_SERIAL_NUMBER: error in reading data")
    return read_data


#************write_MEASURE_CYCLE*********************
#description: set the measurement cycle of the multisensor
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#       time: loop time, in seconds
#output: none
#***************************************************************************   
def write_MEASURE_CYCLE( ser, address,time):
    #check if the serial port is open
    if ser.is_open==False:
        print("write_MEASURE_CYCLE: serial port not open.")
        return 0
    #reset the output buffer before send new data    
    ser.reset_output_buffer   
    out=[address, MODBUS_WRITE_SINGLE_REGISTER, 0x0, MODBUS_STATE_REGISTER_MEASURE_CYCLE, 0, time]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))     
    #send data and read the answer. If any error send the message again before give up.        
    j=0;
    while j<MAX_ITERATION:
        write_message(ser,out,address)
        #read the return message
        read_data=read_message(address, MODBUS_WRITE_SINGLE_REGISTER,ser)
        if not(read_data[0]==0 and len(read_data)==1):
            #force loop exit
            j=MAX_ITERATION+1
        else:
            j=j+1
        
    if read_data[0]==0:
        print("write_MEASURE_CYCLE: error in reading data")
        return read_data
    #if no error return ok
    if (error_in_message_check(read_data)[0]!=0):
        return bytes ([1])
    return bytes ([0])


#************read_MEASUREMENTS****************************
#description: read value of all measure available
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#       measure_number: measure number to dowload
#output: 64 bit number
#**********************************************************************
def read_MEASUREMENTS (ser, address):
    #check if the serial port is open
    if ser.is_open==False:
        print("read_MEASUREMENTS: serial port not open.")
        return bytes ([0])
    #reset the output buffer before send new data 
    ser.reset_output_buffer     
    out=[address, MODBUS_READ_SINGLE_REGISTER, 0x0, MODBUS_DATA_READ_MEASURES, 0, 0]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))       
    #send data and read the answer. If any error send the message again before give up.        
    j=0;
    while j<MAX_ITERATION:         
        write_message(ser,out,address)
        read_data=read_message(address, MODBUS_READ_SINGLE_REGISTER,ser)        
        if not(read_data[0]==0 and len(read_data)==1):
            #force loop exit
            return read_data[4:(len(read_data)-5)]
        else:
            j=j+1         
    print("read_MEASUREMENTS: error in reading data")
    return read_data


#************read_NUMBER_OF_MEASUREMENTS*********************
#description: return the number of available measures (on board sensor
#             and connected AFEs)
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#output: 4 bytes of the resultin string that contains the multisensor
#       serial number
#********************************************************************
def read_NUMBER_OF_MEASUREMENTS(ser, address):
    #check if the serial port is open
    if ser.is_open==False:
        print("read_NUMBER_OF_MEASUREMENTS: serial port not open.")
        return bytes ([0])
    #reset the output buffer before send new data    
    ser.reset_output_buffer
    out=[address, MODBUS_READ_SINGLE_REGISTER, 0x0, MODBUS_DATA_NUMBER_OF_MEASURE, 0, 0]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))       
    #send data and read the answer. If any error send the message again before give up.        
    j=0;
    while j<MAX_ITERATION:   
        write_message(ser,out,address)
        #read the return message
        read_data=read_message(address, MODBUS_READ_SINGLE_REGISTER,ser)
        if not(read_data[0]==0 and len(read_data)==1):
            #the string is valid, check the result. if the data bytes are 0x1 0x0 ready is ok
            return bytes([read_data[4], read_data[5]])
        else:
            j=j+1          
    print("read_NUMBER_OF_MEASUREMENTS: error in reading data")
    return read_data




#************read_MEASUREMENTS_NAME*********************
#description: return the label of the measure number measure_number
#input: system: PC or raspebberry
#       serial_port: serial port variable
#       address: multisensor variable
#       measure number
#output: 10 bytes of measure name
#********************************************************************
def read_MEASUREMENTS_NAME(ser, address,measure_number):
    #check if the serial port is open
    if ser.is_open==False:
        print("read_MEASUREMENTS_NAME: serial port not open.")
        return bytes ([0])
    #reset the output buffer before send new data    
    ser.reset_output_buffer   
    out=[address, MODBUS_READ_SINGLE_REGISTER, 0x0, MODBUS_DATA_MEASURE_NAMES, 0, measure_number]
    #calculate and add the CRC
    out=out + list(struct.pack("<H", libscrc.modbus(bytes(out))))       
    #send data and read the answer. If any error send the message again before give up.        
    j=0;
    while j<MAX_ITERATION: 
        write_message(ser,out,address)
        #read the return message
        read_data=read_message(address, MODBUS_READ_SINGLE_REGISTER,ser)
        if not(read_data[0]==0 and len(read_data)==1):
            return read_data[4:15]
        else:
            j=j+1            
    print("read_MEASUREMENTS_NAME: error in reading data")
    return read_data



class Multisensor_board:
    def __init__(self):
        self.identity = DEVICE_IDENTITY
        self.connection_type = CONNECTION_TYPE
        self.sensors = DEVICE_SENSORS
        self.baud_rate = DEVICE_BAUD_RATE
        self.port = None
        self.portname = ""
        self.num_sensors = 0
        self.sn = ""
        
    def getConnectionParams(self):
        return [self.portname,self.baud_rate]

    def getConnectionType(self):
        return self.connection_type

    def getIdentity(self):
        return self.identity

    def setIdentity(self,idstring):
        self.identity = idstring

    def getSN(self):
        return self.sn
    
    def getSensors(self):
        return self.sensors

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
        if(serport.find("ttyUSB")>=0) or (serport.find("ttyAMA")>=0):
            return found
        try:
            self.port = serial.Serial(serport,self.baud_rate, timeout = SERIAL_TIMEOUT, rtscts=0)
        except Exception as e:
            return found
        data_in=read_SERIAL_NUMBER(self.port, multisensor_address)
        time.sleep(0.1)
        try:
            self.sn = str(int(data_in.hex(),16))
        except Exception as e:
            self.sn = ""
            return found
        res = write_MEASURE_CYCLE(self.port,multisensor_address,0)
        time.sleep(0.2)  
        ww = write_SCAN_AFE(self.port, multisensor_address)
        if ww == 0:
            return found
        time.sleep(0.2)
        multisensor_ready=read_READY(self.port, multisensor_address)
        num_attempt=0
        while (multisensor_ready[0]!=1 and num_attempt<MAX_NUM_ATTEMPT):
            multisensor_ready=read_READY(self.port, multisensor_address)
            time.sleep(0.2)
            num_attempt=num_attempt+1
        num_byte = read_NUMBER_OF_MEASUREMENTS(self.port, multisensor_address)
        self.num_sensors = int.from_bytes(num_byte,byteorder='big', signed=False)
        sensors = []
        for ns in range(1,self.num_sensors+1):
            time.sleep(0.2)
            bytes_out = read_MEASUREMENTS_NAME(self.port, multisensor_address,ns)
            afen = bytes_out[0]
            if afen==0x0B:
                sensors.append(bytes_out[1:15].decode("utf-8").replace('\x00',''))
            else:
                sensors.append("AFE" + str(afen) + "-" + bytes_out[1:15].decode("utf-8").replace('\x00',''))
        self.sensors = ';'.join(sensors)
        self.sensors.replace(' ','')
        self.sensors.replace('_','-')
        res = write_MEASURE_CYCLE(self.port,multisensor_address,3)
        srp = serport.split("/")
        srp1 = srp[-1]
        self.portname = serport
        found = 1
        return found

## the function "sample" reads the sensor output,
## then returns a string separate by semicolon containing data
## if an error happens, it returns the string with err value: "-100.0"
    def sample(self):
        try:
            new_data = read_MEASUREMENTS(self.port, multisensor_address)
            string=""
            for i in range (1, self.num_sensors + 1):
                offset=4*(i-1)+4
                value=bytes(new_data[offset:(offset+4)])
                #unpack the 4 bytes as float nubmer and force big-endian
                [value] = struct.unpack('>f', value)
                string ='{0}{1:03.2f};'.format(string,value)
            string1 = string.rstrip(";")
            return string1
        except Exception as e:
            for i in range (1, self.num_sensors + 1):
                string = string + ERR_VAL + ";"
            return string.rstrip(";")
