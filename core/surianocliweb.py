#!/usr/bin/python
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

import socket
import os, time

## udp socket settings for communications with sentinair system manager
UDP_SERVICE_PORT = 16670
UDP_SERVER_ADDRESS = ('localhost', UDP_SERVICE_PORT)

## end string marker
END_STR = ">>>end__"

### relevant paths for retreiving data files and logs
DATA_PATH = "/var/www/html/data/"
LOG_PATH = "/var/www/html/log/"
STRTOSEEK = "/var/www/html/data/"

## function to ask the current status to the system manager
def query(sck):
    try:
        sent = sck.sendto('i'.encode(), UDP_SERVER_ADDRESS)
        data, server = sck.recvfrom(1024)
        data1 = data.decode()
        data1 = data.rstrip(END_STR)
        return str(data1)
    except:
        return "INSTRUMENTATION MANAGER is taking too much to answer. Try restart!\n"

## function to print in the web page information about the current status
def print_status(msg,mcn):
    l = msg.split(STRTOSEEK)
    if len(l) > 1:
        filen = l[1].rstrip(".")
        print ('<font face = \"courier\"><b>' + l[0] +\
            '</b></font><a target=\"_blank\" href=\"/data/'\
            + filen + '\"><font face = \"courier\"><b>' + filen +\
            '</b></font></a>&nbsp<a href=\"/cgi-bin/fileinspector.py?fn=' + filen +\
            '&mn=' + mcn + '\"><img alt=\"Data plot page\" src=\"/btnplt.png\"></a><br>')
    else:
        print ('<font face = \"courier\"><b>' + msg + '</b></font><br>')
    
## function to build the web page
def webpage(toedit,mn):
    te = toedit.split("\n")
    print ("Content-type:text/html\r\n\r\n")
    print ('<html>')
    print ('<head>')
    print ('<title>' + mn + " status page" + '</title>')
    print ('<style type=\"text/css\"> body { background-image: url(\"/sentinair.jpg\");background-size: cover;}</style>')
    print ('</head>')
    print ('<body><div id=\"main\">')
    print ('<p><h2><font face = \"arial\">' + mn + " status" + '</font></h2>')
    for it in te:
        print_status(str(it),mn)
    print ('</p><br>')
    print ('<p><h2><font face = \"arial\">' + mn + " data" + '</font></h2>')
    try:
        lf = os.listdir(DATA_PATH)
        print ('<table><tr><td><b><font face = \"arial\" size =\"+1\">Data files&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Size&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Last modified</font></b></td><td></td></tr>')
        for l in lf:
            sz = os.stat(DATA_PATH + str(l)).st_size
            tm = time.ctime(os.path.getmtime(DATA_PATH + str(l)))
            print ('<tr><td><a target=\"_blank\" href=\"/data/' +\
                  str(l) + '\"><font face = \"courier\" size =\"+1\"><b>' +\
                  str(l) + '</b></font></a>&nbsp&nbsp&nbsp&nbsp</td><td><font face = \"courier\" size =\"+1\"><b>' +\
                  str(sz) + '&nbsp&nbsp&nbsp&nbsp</b></font></td><td><font face = \"courier\" size =\"+1\"><b>' +\
                  str(tm) + '</b></font></td>' +\
                  '<td>&nbsp<a href=\"/cgi-bin/fileinspector.py?fn=' + str(l) +\
                '&mn=' + mn + '\"><img alt=\"Data plot page\" src=\"/btnplt.png\"></a></td></tr>')
        print ('</table><br></h2></p>')
    except Exception as e:
        print ('<font face = \"courier\" size =\"+1\"><b>Data unavailable due to an internal error!' + str(e) +'</b></font>')
    print ('<p><h2><font face = \"arial\">' + mn + " Log files" + '</font></h2>')
    try:
        lf = os.listdir(LOG_PATH)
        print ('<table><tr><td><b><font face = \"arial\" size =\"+1\">Log files&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Size&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Last modified</font></b></td></tr>')
        for l in lf:
            sz = os.stat(LOG_PATH + str(l)).st_size
            tm = time.ctime(os.path.getmtime(LOG_PATH + str(l)))
            print ('<tr><td><a target=\"_blank\" href=\"/log/' + str(l) + '\"><font face = \"courier\" size =\"+1\"><b>' + str(l) + '</b></font></a>&nbsp&nbsp&nbsp&nbsp</td><td><font face = \"courier\" size =\"+1\"><b>' + str(sz) + '&nbsp&nbsp&nbsp&nbsp</b></font></td><td><font face = \"courier\" size =\"+1\"><b>' + str(tm) + '</b></font></td></tr>')
        print ('</table></h2></p></div>')
    except:
        print ('<font face = \"courier\" size =\"+1\"><b>Logs unavailable due to an internal error!</b></font>')
    print ('<div class=\"foot\"><br><br><br><br><br><br>©2019 SentinAir is a project by Dr. Domenico Suriano</div>')
    print ('</body>')
    print ('</html>')



#########################            
########### MAIN ########
#########################

### retreiving the device name to display in the web page
try:
    f = open("/etc/hostname","r")
    machine_name = f.readline().rstrip("\r\n")
    f.close()
except:
    machine_name = ""

### creation of the udp socket to communicate with the system manager
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(40)
    datastr = query(sock)
    sock.close()
    webpage(datastr,machine_name)
except:
    err = "Fatal error: impossible to communicate with the instrument manager!"
    webpage(err,machine_name)
