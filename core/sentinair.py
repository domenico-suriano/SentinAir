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

import socket
import sys
import _thread
import time

UDP_SERVICE_PORT = 16670
DATA_PORT = 24504
UDP_SERVER_ADDRESS = ('localhost', UDP_SERVICE_PORT)

END_STR = ">>>end__"

### initialization of communication with system manger
### and getting information about sentinair current status
def init(sck):
    try:
        data1 = ""
        sent = sck.sendto('h'.encode(), UDP_SERVER_ADDRESS)
        while (data1.find(END_STR) == -1):
            data, server = sck.recvfrom(1024)
            data1 = data.decode()
        data2 = data1.rstrip(END_STR)
        print (data2)
        print ("INSTRUMENTATION MANAGER by Domenico Suriano ready!\n\r")
    except Exception as e:
        print ("INSTRUMENTATION MANAGER is taking too much to answer. Try restart!\r\n")
        print(str(e))
        sys.exit(0)
    try:
        time.sleep(0.2)
        data6 = ""
        sent = sck.sendto('i'.encode(), UDP_SERVER_ADDRESS)
        while (data6.find(END_STR) == -1):
            data5, server = sck.recvfrom(1024)
            data6 = data5.decode()
            data7 = data6.rstrip(END_STR)
            print(data7)
    except Exception as e:
        print ("INSTRUMENTATION MANAGER is taking too much to answer. Try restart!\r\n")
        print(str(e))   

## function for receiving measures data from system manager
def measure_listener(socktcp):
    while 1:
        try:
            data1,addr = socktcp.recvfrom(1024)
            data2 = data1.decode()
            print ("\r\n" + data2)
            sys.stdout.write("\r\n>>> ")
            sys.stdout.flush()
        except Exception as e:
            print ("Fatal error: impossible to communicate with the instrument manager!")
            print(str(e))
            sys.exit(0)


#######################            
######### MAIN ########
#######################
print ("\r\nINSTRUMENTATION MANAGER by Domenico Suriano opening...\n\r")
## creation of udp sockets for communcations with senstinair system manager
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(40)
    init(sock)
    sck = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sck.bind(('localhost',DATA_PORT))
    _thread.start_new_thread(measure_listener,(sck,))## starting the thread to receive measures data
except Exception as e:
    print ("Fatal error: impossible to communicate with the instrument manager!")
    print(str(e))
    sys.exit(0)
### infinite loop to get user commands
while 1:
    message = input(">>> ")
    if message == "q":
        print ("Exiting from program...\r\n")
        sock.close()
        sys.exit(0)
    try:
        data1 = ""
        data2 = ""
        sent = sock.sendto(message.encode(), UDP_SERVER_ADDRESS)
        while (data2.find(END_STR) == -1):
            data, server = sock.recvfrom(1024)
            data2 = data.decode()
            data1 = data2.rstrip(END_STR)
            print (data1)
    except socket.timeout:
        print ("\r\nThe instrument manager is taking too much to answer. Try again!\r\n")
