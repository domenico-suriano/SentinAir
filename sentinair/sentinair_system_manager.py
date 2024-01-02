# Copyright 2023   Dr. Domenico Suriano (domenico.suriano@enea.it)
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

installed_devices = []
#sps30 has been installed in SentinAir on 2023-12-11_11-13-26
# do not remove or modify the next three lines below!!!
from devices.sps30 import Sps30
sps30_obj = Sps30()
installed_devices.append(sps30_obj)
#v72m has been installed in SentinAir on 2023-12-11_11-13-18
# do not remove or modify the next three lines below!!!
from devices.v72m import V72m
v72m_obj = V72m()
installed_devices.append(v72m_obj)
#co12m has been installed in SentinAir on 2023-12-11_11-13-08
# do not remove or modify the next three lines below!!!
from devices.co12m import Co12m
co12m_obj = Co12m()
installed_devices.append(co12m_obj)
#lcss_adapter has been installed in SentinAir on 2023-12-11_11-13-03
# do not remove or modify the next three lines below!!!
from devices.lcss_adapter import Lcss_adapter
lcss_adapter_obj = Lcss_adapter()
installed_devices.append(lcss_adapter_obj)
#pms3003 has been installed in SentinAir on 2023-12-11_11-12-54
# do not remove or modify the next three lines below!!!
from devices.pms3003 import Pms3003
pms3003_obj = Pms3003()
installed_devices.append(pms3003_obj)
#multisensor_board has been installed in SentinAir on 2023-12-11_11-12-48
# do not remove or modify the next three lines below!!!
from devices.multisensor_board import Multisensor_board
multisensor_board_obj = Multisensor_board()
installed_devices.append(multisensor_board_obj)
#o342 has been installed in SentinAir on 2023-12-11_11-12-36
# do not remove or modify the next three lines below!!!
from devices.o342 import O342
o342_obj = O342()
installed_devices.append(o342_obj)
#mcp342x has been installed in SentinAir on 2023-12-11_11-12-24
# do not remove or modify the next three lines below!!!
from devices.mcp342x import Mcp342x
mcp342x_obj = Mcp342x()
installed_devices.append(mcp342x_obj)
#af22 has been installed in SentinAir on 2023-12-11_11-12-16
# do not remove or modify the next three lines below!!!
from devices.af22 import Af22
af22_obj = Af22()
installed_devices.append(af22_obj)
#nox405 has been installed in SentinAir on 2023-12-11_11-12-04
# do not remove or modify the next three lines below!!!
from devices.nox405 import Nox405
nox405_obj = Nox405()
installed_devices.append(nox405_obj)
#ac32 has been installed in SentinAir on 2023-12-11_11-11-50
# do not remove or modify the next three lines below!!!
from devices.ac32 import Ac32
ac32_obj = Ac32()
installed_devices.append(ac32_obj)
#bh1750 has been installed in SentinAir on 2023-12-11_11-11-43
# do not remove or modify the next three lines below!!!
from devices.bh1750 import Bh1750
bh1750_obj = Bh1750()
installed_devices.append(bh1750_obj)
#pms5003 has been installed in SentinAir on 2023-12-11_11-11-30
# do not remove or modify the next three lines below!!!
from devices.pms5003 import Pms5003
pms5003_obj = Pms5003()
installed_devices.append(pms5003_obj)
#go3 has been installed in SentinAir on 2023-12-11_11-11-21
# do not remove or modify the next three lines below!!!
from devices.go3 import Go3
go3_obj = Go3()
installed_devices.append(go3_obj)
#irca1 has been installed in SentinAir on 2023-12-11_11-11-16
# do not remove or modify the next three lines below!!!
from devices.irca1 import Irca1
irca1_obj = Irca1()
installed_devices.append(irca1_obj)
#mhz19 has been installed in SentinAir on 2023-12-11_11-11-09
# do not remove or modify the next three lines below!!!
from devices.mhz19 import Mhz19
mhz19_obj = Mhz19()
installed_devices.append(mhz19_obj)
#bme280 has been installed in SentinAir on 2020-12-15_10-00-51
from devices.bme280 import Bme280
bme280_obj = Bme280()
installed_devices.append(bme280_obj)
# do not remove or modify the next three lines below!!!
# do not remove or modify the next three lines below!!!
# do not remove or modify the next three lines below!!!

import copy
import serial.tools.list_ports
import serial
import time
import _thread
import logging
import RPi.GPIO as GPIO
import socket
import sys
from datetime import datetime
from urllib.parse import urlparse
import os
import base64
import http.server
import threading
import mimetypes
import pandas as pd
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import cgi
#graphic management libraries
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as dates
#end

#connected devices are stored here
connected_devices = []

#sentinair files paths
HOME_DIR = "/home/pi/sentinair/"
LOG_DIR = "logs/"
DATA_DIR = "data/"
AVG_DIR = "avg/"
IMG_DIR = "img/"
PLOT_DIR = "plots/"
LOG_FILENAME = 'sentinair-log.txt'
IMAP_SMTP_FILE = HOME_DIR + "imap-smtp-interface.py"
MAIL_CONFIG_FILE = HOME_DIR + "mail-config.sentinair"
DATA_PATH = "/data/"
LOG_PATH = "/logs/"
IMG_PATH = "/img/"
PLOT_PATH = "/plots/"
AVG_PATH = "/avg/"

#connection types of devices
USB_CONNECTION_TYPE = "usb"
SERIAL_CONNECTION_TYPE = "serial"
ETH_CONNECTION_TYPE = "eth"
SPI_CONNECTION_TYPE = "spi"
I2C_CONNECTION_TYPE = "i2c"

#messages to send to user interfaces
INIT_LOG_MSG = 'SENTINAIR MANAGER by Domenico Suriano setting up...'
INIT_GPIO_ERR_LOG_MSG = 'Error in initializing GPIO:'
SHUTDOWN_BUTTON_PRESSED = 'SentinAir shut down by stop button pressed'
UDP_CLI_PORT_ERR_LOG_MSG = 'Unable to start SentinAir command line user interface: udp port not opening! '
UDP_CLI_DATA_ERR_LOG_MSG = 'Error in opening data channel: udp port not opening'
DATA_SERVER_ERR_LOG_MSG = 'Error in starting data server.'
DATA_SERVER_PORT_ERR_LOG_MSG = 'Unable to start the SentinAir data server: data port not opening.'
DATA_SENDING_ERR_LOG_MSG = 'Unable to send measurement on data port.'
CMD_IN_ERR_LOG_MSG = 'Unable to get commands on udp port:'
CMD_OUT_ERR_LOG_MSG = 'Unable to send commands outputs on udp port:'
STATUS_FILE_ERR_LOG_MSG = 'Unable to update status file:'
INIT_CAPT_GPIO_ERR_LOG_MSG_1 = 'GPIO error on init capture 1:'
INIT_CAPT_GPIO_ERR_LOG_MSG_2 = 'GPIO error on init capture 2:'
INIT_CAPT_GPIO_ERR_LOG_MSG_3 = 'GPIO error on init capture 3:'
INIT_CAPT_ERR_LOG_MSG = 'Error occurred on init_session:'
INIT_CAPT_MAKE_ERR_LOG_MSG = 'Error on make_record in init capture:'
MAKE_ERR_LOG_MSG = 'Error on make_record capture:'
SYS_READY_LOG_MSG = 'SentinAir ready!'
DATA_PORT_OPEN_ERR_LOG_MSG = "Udp data port opening failed"
MAIL_CONFIG_NULL_LOG_MSG = "E-mail account is not present: the imap-smtp interface will not start"
INIT_WEB_SERVER_SERVICES = "Unable to correctly start server web services "
INIT_LOG_FILE_ERROR = "Failed to open the log file. Program killed!"

INIT_MSG = "\n\n" + INIT_LOG_MSG + "\n"
UDP_CLI_PORT_ERR_MSG = "\n" + UDP_CLI_PORT_ERR_LOG_MSG + "\n"
INIT_GPIO_ERR_MSG = "\n" + INIT_GPIO_ERR_LOG_MSG + '\n'
UDP_CLI_PORT_ERR_MSG = "\n" + UDP_CLI_PORT_ERR_LOG_MSG + "\n"
DATA_SERVER_ERR_MSG = "\n" + DATA_SERVER_ERR_LOG_MSG + "\n"
DATA_SERVER_PORT_ERR_MSG = "\n" + DATA_SERVER_PORT_ERR_LOG_MSG + "\n"
DATA_SENDING_ERR_MSG = "\n" + DATA_SENDING_ERR_LOG_MSG + "\n"
DATA_FILE_OPENING_ERR = "\nImpossible opening storage data file. Measurement sesssion stopped with error"
MEAS_STOP_ERR_MSG = "\nMeasurement session stopped with error"
SYS_READY = "\n" + SYS_READY_LOG_MSG + "\n"
INV_CMD = "\nCommand not valid!\n"
DATA_PORT_OPEN_ERR_MSG = "\n" + DATA_PORT_OPEN_ERR_LOG_MSG + "\n"
MAIL_CONFIG_NULL = "\nE-mail account is not present: the imap-smtp interface will not start\n"


ERRS_STR = "Impossible to execute the command.\n" +\
           "Monitoring underway,\n" + "if you want to execute it\n" +\
           "first press 'b' to stop the session!\n"
ERRC_STR = "Impossible to execute the command.\n" +\
           "Monitoring underway,\n" + "if you want to check on devices\n" +\
           "first press 'b' to stop the session!\n"
ERRS_STR_1 = "Impossible to execute the command:\n" +\
             "no device connected,\n" + "if you want to execute it\n" +\
             "first press 's' to search and connect them!\n"
USAGE_STR = "press i[ENTER] to get info on the current status\n" +\
            "press q[ENTER] to quit the command consolle \n" +\
            "press h[ENTER] for command viewing\n" +\
            "press s[ENTER] for searching devices\n" +\
            "press c[ENTER] for checking devices\n" +\
            "press b[ENTER] for stopping sampling sessions\n" +\
            "press s,<sampling rate in seconds>[ENTER] to start and log a sampling session\n"
NO_MEAS = "No measurement session ongoing"

#strings markers
__ERROR = "__error"
END_STR = ">>>end__"
PANEL_STRIP_STRING = "Data storage file"

#system settings
MINIMUM_SAMPLING_RATE = 30
UDP_SERVICE_PORT = 16670
UDP_HOST_BINDING = '0.0.0.0'
DATA_PORT = 24504
DATA_ADDRESS = ('localhost', DATA_PORT)
BUFSIZE = 1024
HOST = 'localhost'
UDP_SERVER_ADDRESS = (HOST, UDP_SERVICE_PORT)

#########################################################
##### class related to the web server services ##########
##### and routines to make it work ######################
#########################################################
class Handler(http.server.SimpleHTTPRequestHandler):

    ##### this function overrides the parent method to
    ##### suppress log messages on the cli
    def log_message(self, format, *args):
        pass
    ####################################################
    ####################################################

    
    def send_command(self,com):
        global ssock
        try:
            data1 = ""
            data2 = ""
            sent = ssock.sendto(com.encode(), UDP_SERVER_ADDRESS)
            while (data2.find(END_STR) == -1):
                data, server = ssock.recvfrom(1024)
                data2 = data.decode()
                data1 = data1 + data2.rstrip(END_STR)
            return data1
        except socket.timeout:
            logging.warning("Server rrror occurred in executing GET!\n ",exc_info=True)
            return "\r\nThe instrument manager is taking too much to answer. Try again!\r\n"


    def index_msgentry_format(self,msg1):
        te = msg1.split("\n")
        msgentry = ""
        for it in te:
            if it.find(HOME_DIR + DATA_DIR) >= 0:
                l = it.split(HOME_DIR + DATA_DIR)
                msgentry = msgentry + '<font face = \"courier\"><b>' + l[0] +\
                    '</b></font><a target=\"_blank\" href=\"' + DATA_PATH +\
                    l[1] + '\"><font face = \"courier\"><b>' + l[1] +\
                    '</b></font></a><br><a href=\"/plotmaker?fn=' + l[1] +\
                    '\"><img alt=\"Data plot page\" src=\"' + IMG_PATH +\
                    'btnplt.png\"></a>&nbsp<a href=\"/havg?fn=' + l[1] +\
                    '\"><img alt=\"Data hourly averages\" src=\"' + IMG_PATH +\
                    'havg.png\"></a>&nbsp<a href=\"/davg?fn=' + l[1] +\
                    '\"><img alt=\"Data daily averages\" src=\"' + IMG_PATH +\
                    'davg.png\"></a><br>'
            else:
                msgentry = msgentry + '<font face = \"courier\"><b>' + it + '</b></font><br>'
        return msgentry
    

    def index(self,msg1):
        head1 = "<html><head><title>" + machine_name + " status page</title>"
        head2 = "<style> body { background-image: url(\'" + IMG_PATH + "sentinair.png\');background-size: cover;}</style></head>"
        body1 = "<body><div id=\"main\"><p></p><h2><font face=\"arial\">" + machine_name + " status</font></h2>"
        msgentry = self.index_msgentry_format(msg1)
        body2 = '<table><tr><td><b><font face = \"arial\" size =\"+1\">Data files&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Size&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Last modified</font></b></td><td></td></tr>'
        lf = os.listdir(HOME_DIR + DATA_DIR)
        filelist = ""
        for l in lf:
            sz = os.stat(HOME_DIR + DATA_DIR + str(l)).st_size
            tm = time.ctime(os.path.getmtime(HOME_DIR + DATA_DIR + str(l)))
            filelist = filelist + '<tr><td><a target=\"_blank\" href=\"' + DATA_PATH +\
                  str(l) + '\"><font face = \"courier\" size =\"+1\"><b>' +\
                  str(l) + '</b></font></a>&nbsp&nbsp&nbsp&nbsp</td><td><font face = \"courier\" size =\"+1\"><b>' +\
                  str(sz) + '&nbsp&nbsp&nbsp&nbsp</b></font></td><td><font face = \"courier\" size =\"+1\"><b>' +\
                  str(tm) + '</b></font></td>' +\
                  '<td>&nbsp<a href=\"/plotmaker?fn=' + str(l) +\
                '\"><img alt=\"Data plot page\" src=\"' + IMG_PATH +\
                'btnplt.png\"></a><br>&nbsp<a href=\"/havg?fn=' + str(l) +\
                '\"><img alt=\"Hourly averages\" src=\"' + IMG_PATH +\
                'havg.png\"></a><br>&nbsp<a href=\"/davg?fn=' + str(l) +\
                '\"><img alt=\"Daily averages\" src=\"' + IMG_PATH +\
                'davg.png\"></a></td></tr>'
        filelist = filelist + '</table><br></h2></p>'
        body3 = '<p><h2><font face = \"arial\">' + machine_name + " Log files" + '</font></h2>'
        lf = os.listdir(HOME_DIR + LOG_DIR)
        body4 = '<table><tr><td><b><font face = \"arial\" size =\"+1\">Log files&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Size&nbsp&nbsp&nbsp&nbsp</font></b></td><td><b><font face = \"arial\" size =\"+1\">Last modified</font></b></td></tr>'
        logfiles = ""
        for l in lf:
            sz = os.stat(HOME_DIR + LOG_DIR + str(l)).st_size
            tm = time.ctime(os.path.getmtime(HOME_DIR + LOG_DIR + str(l)))
            logfiles = logfiles + '<tr><td><a target=\"_blank\" href=\"' + LOG_PATH +\
                       str(l) + '\"><font face = \"courier\" size =\"+1\"><b>' + str(l) +\
                       '</b></font></a>&nbsp&nbsp&nbsp&nbsp</td><td><font face = \"courier\" size =\"+1\"><b>' +\
                       str(sz) + '&nbsp&nbsp&nbsp&nbsp</b></font></td><td><font face = \"courier\" size =\"+1\"><b>' +\
                       str(tm) + '</b></font></td></tr>'
        logfiles = logfiles + '</table></h2></p></div>'
        config = '<div><p><h2><font face = \"arial\">Restricted area</font></h2>' +\
        '<a target=\"_blank\" href=\"/panel.html\"><img alt=\"Configuration page\" src=\"'\
                 + IMG_PATH + 'conf.png\"></a></div>' 
        body5 = '<div class=\"foot\"><br><br><br><br><br><br>©2019 SentinAir is a project by Dr. Domenico Suriano</div></body></html>'
        self.wfile.write(bytes(head1 + head2 + body1 + msgentry + body2 +\
                               filelist + body3 + body4 + logfiles + config + body5,encoding='utf-8'))


    def panel_msgentry_format(self,msg1):
        te = msg1.split("\n")
        msgentry = ""
        for it in te:
            if it.find(PANEL_STRIP_STRING) < 0:
                msgentry = msgentry + '<font face = \"courier\"><b>' + it + '</b></font><br>'
        return msgentry


    def purge(self):
        try:
            out1 = os.system("rm " + HOME_DIR + DATA_DIR + "*")
            out2 = os.system("rm " + HOME_DIR + PLOT_DIR + "*")
            out3 = os.system("rm " + HOME_DIR + AVG_DIR + "*")
            ll = 0
            try:
                lf = open(HOME_DIR + LOG_DIR + LOG_FILENAME, "w")
                lfstr = lf.write("")
                lf.close()
            except:
                ll = 1
            pp = os.listdir(HOME_DIR + PLOT_DIR)
            aa = os.listdir(HOME_DIR + AVG_DIR)
            dd = os.listdir(HOME_DIR + DATA_DIR)
            if len(dd) != 0:
                return "Some files could not be deleted in the DATA directory"
            if len(pp) != 0:
                return "Some files could not be deleted in the PLOTS directory"
            if len(aa) != 0:
                return "Some files could not be deleted in the AVG directory"
            if ll != 0:
                return "The log file could not be cleaned in the LOGS directory"
            return "All data and log files have been successfully deleted!"
        except Exception as e:
            return "Error in deleting data and log files:\n" + str(e)
      

    def confirm_purge(self):
        head1 = "<html><head><title> Confirm deletion page</title>"
        head2 = "<style> body { background-image: url('/img/sentinair.png');background-size: cover;}</style></head>"
        body1 = "<body><p><h2><font face = \"arial\">WARNING! By pressing the \"Confirm deletion\" button, all data and log files will be permanently deleted!</font></h2></p>"
        body1 += '<a href=\"/panel.html?com=confirmpurge\"><img alt=\"Clean up memory and permanently delete all data files\" src=\"'\
                     + IMG_PATH + 'confirmpurge.png\"></a><br><br>'
        body1 += '<a href=\"/panel.html\"><img alt=\"Get back to the control panel\" src=\"'\
                     + IMG_PATH + 'cancelpurge.png\"></a><br><br>'
        endpage = "</body></html>"
        self.wfile.write(bytes(head1 + head2 + body1 + endpage,encoding='utf-8'))


    def panel(self,answ):
        global rate
        head1 = "<html><head><title>" + machine_name + " configuration page</title>"
        head2 = "<style> body { background-image: url('/img/sentinair.png');background-size: cover;}</style></head>"
        body1 = "<body><p><h2><font face = \"arial\">Control panel of " + machine_name + "</font></h2></p><br>"
        command_answer = self.panel_msgentry_format(answ)
        body1 += command_answer + "<br>"
        body2 = ""
        body3 = ""
        body4 = ""
        if rate > 0:
            body2 += '<a href=\"/panel.html?com=stop\"><img alt=\"Stop monitoring\" src=\"' + IMG_PATH +\
                'stop.png\"></a>'
        else:
            body2 += "<form action=\"start\" method=\"post\"><label for=\"newrate\">Sampling rate (sec):  </label>"
            body2 += "<input type=\"number\" id=\"newrate\" name=\"newrate\" value=\"60\">"
            body2 += "<input type=\"submit\" value=\"Start new monitoring session\"></form><br>"
            body2 += '<a href=\"/panel.html?com=scan\"><img alt=\"Searching for new devices\" src=\"' + IMG_PATH +\
                'scan.png\"></a>'
            body3 += "<p><h2><font face = \"arial\">Set the current system time/date</font></h2></p>"
            body3 += "<form action=\"setdate\" method=\"post\"><label for=\"datetime\">Date/time:  </label>"
            body3 += "<input type=\"datetime-local\" id=\"datetime\" name=\"datetime\">&nbsp"
            body3 += "<input type=\"submit\" value=\"Set date and time\"></form>"
            body4 += "<p><h2><font face = \"arial\">Press the button below to delete all data and log files</font></h2></p>"
            body4 += '<a href=\"/panel.html?com=purge\"><img alt=\"Clean up memory and delete all data files\" src=\"'\
                     + IMG_PATH + 'purge.png\"></a>'
        passchange = "<br><br><p><h2><font face = \"arial\">Password to enter in the restricted area modification</font></h2></p>"
        passchange += "<form action=\"changepass\" method=\"post\"><label for=\"oldpass\">Old password:  </label>"
        passchange += "<input type=\"password\" id=\"oldpass\" name=\"oldpass\"><br>"
        passchange += "<label for=\"newpass\">New password:  </label><input type=\"password\" id=\"newpass\" name=\"newpass\"><br>"
        passchange += "<label for=\"rnewpass\">Re-type new password:  </label><input type=\"password\" id=\"rnewpass\" name=\"rnewpass\"><br>"
        passchange += "<input type=\"submit\" value=\"Modify the password\"></form>"
        endpage = "</body></html>"
        self.wfile.write(bytes(head1 + head2 + body1 + body2 + passchange + body3 + body4 + endpage,encoding='utf-8'))


    def make_averages(self,fn,avgtype):
        errors = ""
        fn1 = fn.replace(HOME_DIR + DATA_DIR,"")
        try:
            if avgtype == 'h':
                mark = 'H'
                file_prefix = "hourly_avg_"
            else:
                mark = 'D'
                file_prefix = "daily_avg_"            
            df = pd.read_csv(fn,sep=";",parse_dates=['Date-time'],index_col=['Date-time'],dayfirst=True)
            avg = df.resample(mark).mean()
            if avgtype == 'h':
                avg.index = pd.to_datetime(avg.index,format='%Y-%m-%d %H')
                avg.index = avg.index.strftime('%Y-%m-%d %H')
            else:
                avg.index = pd.to_datetime(avg.index,format='%Y-%m-%d')
                avg.index = avg.index.strftime('%Y-%m-%d')                
            avg.reset_index(inplace=True)
            avg = avg.rename(columns = {'index':'Date-time'})
            avg.to_csv(HOME_DIR + AVG_DIR + file_prefix + fn1,sep=";",float_format='%.1f',index=False)
        except Exception as e:
            errors = errors + str(e)
        return errors,file_prefix + fn1


    #routine for plotting data of the measurements file
    def plot_file(self,filename,mode):
        #### loading data from file
        datacols = []
        errors = ""
        header = []
        try:
            f = open(filename,"r")
            lines = f.readlines()
            header = lines[0].rstrip("\n").split(";")
        except Exception as e:
            errors = errors + "Error in making plots: " + str(e) + " on file: " + filename
            return errors, header    
        for cols in header:
            datacols.append([])
        numline = 1
        try:
            for line in lines:
                row = lines[numline].rstrip("\n").split(";")
                i = 0
                for cols in header:
                    datacols[i].append(row[i])
                    i += 1
                numline +=1
        except:
            pass
        #### preparing plots
        if mode == 'h':
            fn = filename.rstrip(".txt").replace(HOME_DIR + AVG_DIR,"")
            x1 = [datetime.strptime(d,"%Y-%m-%d %H") for d in datacols[0]]
            hfmt = mpl.dates.DateFormatter("%Y-%m-%d %H")
        elif mode == 'd':
            fn = filename.rstrip(".txt").replace(HOME_DIR + AVG_DIR,"")
            x1 = [datetime.strptime(d,"%Y-%m-%d") for d in datacols[0]]
            hfmt = mpl.dates.DateFormatter("%Y-%m-%d")
        else:
            fn = filename.rstrip(".txt").replace(HOME_DIR + DATA_DIR,"")
            x1 = [datetime.strptime(d,"%Y-%m-%d %H:%M:%S") for d in datacols[0]]
            hfmt = mpl.dates.DateFormatter("%Y-%m-%d %H:%M:%S")
        x = mpl.dates.date2num(x1)
        j = 0
        for cols in header:
            if j == 0:
                j=j+1
                continue
            try:
                fig = plt.figure()
                graph = fig.add_subplot(111)
                graph.xaxis.set_major_formatter(hfmt)
                red_patch = mpatches.Patch(color='red', label=header[j])
                graph.legend(handles=[red_patch])
                y = list(map(float,datacols[j]))
                graph.plot(x,y,'r')
                plt.setp(graph.get_xticklabels(), rotation=30, ha="right")
                if numline > 10:
                    graph.xaxis.set_major_locator(plt.MaxNLocator(10))
                    graph.yaxis.set_major_locator(plt.MaxNLocator(10))
                else:
                    graph.xaxis.set_major_locator(plt.LinearLocator(numticks=(numline-1)))
                    graph.yaxis.set_major_locator(plt.LinearLocator(numticks=(numline-1)))
                text = graph.annotate("Plotted by Sentinair device\n developed by\n Dr. Domenico Suriano 2019",\
                                              xy=(.3,.3),xycoords='figure fraction',rotation=-30,size=16,alpha=0.2)
                graph.grid(True)
                header[j] = header[j].replace('%','')
                header[j] = header[j].replace('/','')
                fig.savefig(HOME_DIR + PLOT_DIR + fn + "." + header[j] + ".png",dpi=80,format='png',bbox_inches='tight')
                plt.close('all')
            except Exception as e:
                errors = errors + "Error in making plots: " + str(e) + " on file: " + filename
                return errors,header
            j=j+1
        return errors,header


    def get_headers(self,filename):
        RETRY = 2
        attempt = 0
        headers = []
        while attempt<RETRY:
            try:
                f = open(filename,'r')
                line = f.readline().rstrip("\n")
                headers = line.split(";")
                f.close()
                return headers
            except:
                attempt += 1
        return headers

        
    def file_plot_page(self,fn,heads):
        fn1 = fn.replace(HOME_DIR + DATA_DIR,"").rstrip(".txt")
        pagestub4 = "<html><head><title>Measure page in file " + fn1 + " on " + machine_name + "</title>"
        pagestub5 = "<style> body { background-image: url(\'" + IMG_PATH + "sentinair.png\');background-size: cover;}</style></head><body>"
        tablerow = ""
        endpage = '</body></html>'
        try:
            tablerow = tablerow + '<p><h2><font face = \"arial\"> Here below are plots from<br>' +\
                    fn1 + '<br>on<br>' + machine_name + '</font></h2></p><table>'
            hnum = 0
            for h in heads:
                if hnum == 0:
                    hnum=hnum+1
                else:
                    tablerow = tablerow + '<tr><td>'
                    h=h.replace('%','')
                    h=h.replace('/','')
                    tablerow = tablerow + '<img alt=\"Data plot unavailable\" src=\"' + PLOT_PATH + fn1 + "." + h + '.png\">'
                    tablerow = tablerow + '</td></tr>'
                    hnum=hnum+1
            tablerow = tablerow + '</table>'
        except Exception as e:
            tablerow = tablerow + '<br>' + str(e) + '<br>' + '</table>'
        self.wfile.write(bytes(pagestub4 + pagestub5 + tablerow + endpage, encoding='utf-8'))


    def avg_plot_page(self,fn,heads,avgtype):
        fn1 = fn.replace(HOME_DIR + AVG_DIR,"").rstrip(".txt")
        if avgtype == 'h':
            pagestub4 = "<html><head><title>Hourly averages of " + fn1 + " on " + machine_name + "</title>"
        else:
            pagestub4 = "<html><head><title>Daily averages of " + fn1 + " on " + machine_name + "</title>"
        pagestub5 = "<style> body { background-image: url(\'" + IMG_PATH + "sentinair.png\');background-size: cover;}</style></head><body>"
        tablerow = ""
        endpage = '</body></html>'
        try:
            tablerow = tablerow + '<p><h2><font face = \"arial\"> Here below are plots from <br>' +\
                   '<a target=\"_blank\" href=\"' + AVG_PATH + fn1 + '.txt\"><font face = \"courier\"><b>' +\
                   fn1 + '</b></font></a>' +'<br>on<br>' + machine_name + '</font></h2></p><table>'
            hnum = 0
            for h in heads:
                if hnum == 0:
                    hnum=hnum+1
                else:
                    tablerow = tablerow + '<tr><td>'
                    h=h.replace('%','')
                    h=h.replace('/','')
                    tablerow = tablerow + '<img alt=\"Data plot unavailable\" src=\"' + PLOT_PATH + fn1 + "." + h + '.png\">'
                    tablerow = tablerow + '</td></tr>'
                    hnum=hnum+1
            tablerow = tablerow + '</table>'
        except Exception as e:
            tablerow = tablerow + '<br>' + str(e) + '<br>' + '</table>'
        self.wfile.write(bytes(pagestub4 + pagestub5 + tablerow + endpage, encoding='utf-8'))


    def settime(self,dt):
        try:
            datet = str(dt).replace("T"," ")
            if datet.find("invalid")>= 0:
                msg = "Invalid date or time!\n Date and time not set!"
                return msg           
            datet = datet + ":00"
            com = 'date -s ' + "\'" + datet + "\'"
            out = os.popen(com).read()
            if out != "":
                msg = "Date and time successfully set to:\n" + out 
                return msg
            msg = "Invalid date or time!\n Date and time not set!"
            return msg
        except Exception as e:
            msg = "An error occurred in setting time and date\n"
            return msg + str(e)

    def no_auth(self):
        page = '<html><head><meta http-equiv=\"refresh\" content=\"0; url=/\"/></head>'
        self.wfile.write(bytes(page,encoding='utf-8'))

    def wrong_pass(self):
        head1 = "<html><head><title>" + machine_name + " status page</title>"
        head2 = "<style> body { background-image: url('/img/sentinair.png');background-size: cover;}</style></head>"
        body1 = "<body><p><h2><font face = \"arial\">PASSWORD OR USER<br>NOT VALID!!!</font></h2></p><br></body></html>"
        self.wfile.write(bytes(head1 + head2 + body1,encoding='utf-8'))

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm=\"/"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def no_file(self):
        head1 = "<html><head><title>" + machine_name + " status page</title>"
        head2 = "<style> body { background-image: url('/img/sentinair.png');background-size: cover;}</style></head>"
        body1 = "<body><p><h2><font face = \"arial\">FILE EMPTY OR NO MORE PRESENT IN THE SYSTEM!!!</font></h2></p><br></body></html>"
        self.wfile.write(bytes(head1 + head2 + body1,encoding='utf-8'))        

    def do_GET(self):
        global encstr
        try:
            urlpath = urlparse(self.path)[2]
            urlquery = urlparse(self.path)[4]
            if (urlpath.endswith(".txt")) and (urlquery == ""):
                file = '.' + str(self.path)
                self.send_response(200)
                try:
                    if os.stat(file).st_size == 0:
                        self.no_file()
                        return
                    self.wfile.write(open(file, 'rb').read())
                    return
                except Exception as e:
                    self.no_file()
                    return
            if urlpath.endswith(".png") or (urlpath == "/favicon.ico"):
                imgname = self.path
                imgname = imgname[1:]
                try:
                    imgfile = open(imgname, 'rb').read()
                    mimetype = mimetypes.MimeTypes().guess_type(imgname)[0]
                except:
                    imgfile = open(HOME_DIR + IMG_DIR + "file_not_found.png", 'rb').read()
                    mimetype = mimetypes.MimeTypes().guess_type("file_not_found.png")[0]
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                try:
                    self.wfile.write(imgfile)
                except:
                    pass
                return  
            if urlpath == "/":
                self.send_response(200)
                ans = self.send_command('i')
                self.index(ans)
                return
            if urlpath == "/plotmaker":
                self.send_response(200)
                qp = urlquery.split("=")
                hd = self.get_headers(HOME_DIR + DATA_DIR + str(qp[1]))
                self.file_plot_page(HOME_DIR + DATA_DIR + str(qp[1]),hd)
                return
            if urlpath == "/havg":
                self.send_response(200)
                qp = urlquery.split("=")
                hd = self.get_headers(HOME_DIR + DATA_DIR + str(qp[1]))
                self.avg_plot_page(HOME_DIR + AVG_DIR + "hourly_avg_" + str(qp[1]),hd,'h')
                return
            if urlpath == "/davg":
                self.send_response(200)
                qp = urlquery.split("=")
                hd = self.get_headers(HOME_DIR + DATA_DIR + str(qp[1]))
                self.avg_plot_page(HOME_DIR + AVG_DIR + "daily_avg_" + str(qp[1]),hd,'d')
                return
            if urlpath == "/panel.html":
                base64_bytes1 = base64.b64decode(encstr)
                idpass1 = base64_bytes1.decode('ascii')
                if self.headers.get("Authorization") == None:
                    self.do_AUTHHEAD()
                    self.no_auth()
                    return
                if self.headers.get("Authorization") == 'Basic ' + str(encstr):
                    self.send_response(200)
                    if(urlquery=="com=stop"):
                        ans = self.send_command('b')
                    elif(urlquery=="com=scan"):
                        ans = self.send_command('s')
                    elif(urlquery=="com=purge"):
                        self.confirm_purge()
                        return
                    elif(urlquery=="com=confirmpurge"):
                        ans = self.purge()
                    else:
                        ans = self.send_command('i')
                    self.panel(ans)
                    return
                else:
                    self.do_AUTHHEAD()
                    self.wrong_pass()
        except Exception as e:
            #print("Server error occurred in executing GET method! " + str(e))
            logging.warning("Server error occurred in executing GET method! ",exc_info=True)


    def do_POST(self):
        global user
        global passwd
        global encstr
        try:
            form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'POST',\
                         'CONTENT_TYPE': self.headers['Content-Type'],})        
            if self.path == "/setdate":
                dt1 = str(form.getvalue("datetime"))        
                res = self.settime(dt1)
                self.panel(res)
                return
            if self.path == "/changepass":
                oldpass = form.getvalue("oldpass")
                newpass = form.getvalue("newpass")
                rnewpass = form.getvalue("rnewpass")
                if (newpass is None) or (rnewpass is None):
                    msg = "Password change failed: empty fields are not allowed"
                    self.panel(msg)
                    return
                if oldpass != passwd:
                    msg = "Password change failed: the old password is wrong!"
                else:
                    if newpass != rnewpass:
                        msg = "Password change failed: please, re-type correctly the new password!"
                    else:
                        msg = "Password successfully changed!"
                        passwd = newpass
                        tostore = user + ":" + newpass
                        data_bytes = tostore.encode('ascii')
                        idpassencoded = base64.b64encode(data_bytes)
                        f = open("pass","wb")
                        f.write(idpassencoded)
                        f.close()
                        encstr = idpassencoded.decode('ascii')
                self.panel(msg)
                return
            if self.path == "/start":
                newrate = form.getvalue("newrate")
                try:
                    nr = int(newrate)
                except:
                    ans = "Impossible to start a new monitoring session:\nplease select an integer value as sampling rate!"
                    self.panel(ans)
                    return
                ans = self.send_command('s,' + newrate)
                self.panel(ans)
                return
            ans = self.send_command('i')
            self.panel(ans)
        except Exception as e:
            #print("Server error occurred in executing POST method! " + str(e))
            logging.warning("Server error occurred in executing POST method! ",exc_info=True)    

########################################################
########################################################


############# GRAPHIC ######################
##### routine for plots generation
############################################

def plotter(filename):
    global rate
    HOUR_SEC = 3600
    DAY_SEC = 86400
    try:
        now = int(time.time())
        nowh = now
        nowd = now
        while rate > 0:
            time.sleep(1)
            then = int(time.time())
            d = then - now
            dh = then - nowh
            dd = then - nowd
            if d >= rate:
                now = then
                plot_file(filename,'f')
            if dh >= HOUR_SEC:
                nowh = then
                fn = make_averages(filename,'h')
                plot_file(fn,'h')
            if dd >= DAY_SEC:
                nowd = then
                fn = make_averages(filename,'d')
                plot_file(fn,'d')
    except Exception as e:
        logging.warning("Error occurred in plotting service. Data plotting stopped! " + str(e))
            

#routine for plotting data of the measurements file
def plot_file(filename,mode):
    global rate
    #### loading data from file
    datacols = []
    header = []
    try:
        f = open(filename,"r")
        lines = f.readlines()
        header = lines[0].rstrip("\n").split(";")
    except Exception as e:
        logging.warning("Error in making plots: " + str(e) + " on file: " + filename)
        return 
    for cols in header:
        datacols.append([])
    numline = 1
    try:
        for line in lines:
            row = lines[numline].rstrip("\n").split(";")
            i = 0
            for cols in header:
                datacols[i].append(row[i])
                i += 1
            numline +=1
    except:
        pass
    #### preparing plots
    if mode == 'h':
        fn = filename.rstrip(".txt").replace(HOME_DIR + AVG_DIR,"")
        x1 = [datetime.strptime(d,"%Y-%m-%d %H") for d in datacols[0]]
        hfmt = mpl.dates.DateFormatter("%Y-%m-%d %H")
    elif mode == 'd':
        fn = filename.rstrip(".txt").replace(HOME_DIR + AVG_DIR,"")
        x1 = [datetime.strptime(d,"%Y-%m-%d") for d in datacols[0]]
        hfmt = mpl.dates.DateFormatter("%Y-%m-%d")
    else:
        fn = filename.rstrip(".txt").replace(HOME_DIR + DATA_DIR,"")
        x1 = [datetime.strptime(d,"%Y-%m-%d %H:%M:%S") for d in datacols[0]]
        hfmt = mpl.dates.DateFormatter("%Y-%m-%d %H:%M:%S")
    x = mpl.dates.date2num(x1)
    j = 0
    for cols in header:
        if rate == 0:
            break
        if j == 0:
            j=j+1
            continue
        try:
            fig = plt.figure()
            graph = fig.add_subplot(111)
            graph.xaxis.set_major_formatter(hfmt)
            red_patch = mpatches.Patch(color='red', label=header[j])
            graph.legend(handles=[red_patch])
            y = list(map(float,datacols[j]))
            graph.plot(x,y,'r')
            plt.setp(graph.get_xticklabels(), rotation=30, ha="right")
            if numline > 10:
                graph.xaxis.set_major_locator(plt.MaxNLocator(10))
                graph.yaxis.set_major_locator(plt.MaxNLocator(10))
            else:
                graph.xaxis.set_major_locator(plt.LinearLocator(numticks=(numline-1)))
                graph.yaxis.set_major_locator(plt.LinearLocator(numticks=(numline-1)))
            text = graph.annotate("Plotted by Sentinair device\n developed by\n Dr. Domenico Suriano 2019",\
                                          xy=(.3,.3),xycoords='figure fraction',rotation=-30,size=16,alpha=0.2)
            graph.grid(True)
            header[j] = header[j].replace('%','')
            header[j] = header[j].replace('/','')
            fig.savefig(HOME_DIR + PLOT_DIR + fn + "." + header[j] + ".png",dpi=80,format='png',bbox_inches='tight')
            plt.close('all')
        except Exception as e:
            logging.warning("Error in making plots: " + str(e) + " on file: " + filename)
            return
        j=j+1


def make_averages(fn,avgtype):
    fn1 = fn.replace(HOME_DIR + DATA_DIR,"")
    try:
        if avgtype == 'h':
            mark = 'H'
            file_prefix = "hourly_avg_"
        else:
            mark = 'D'
            file_prefix = "daily_avg_"            
        df = pd.read_csv(fn,sep=";",parse_dates=['Date-time'],index_col=['Date-time'],dayfirst=True)
        avg = df.resample(mark).mean()
        if avgtype == 'h':
            avg.index = pd.to_datetime(avg.index,format='%Y-%m-%d %H')
            avg.index = avg.index.strftime('%Y-%m-%d %H')
        else:
            avg.index = pd.to_datetime(avg.index,format='%Y-%m-%d')
            avg.index = avg.index.strftime('%Y-%m-%d')                
        avg.reset_index(inplace=True)
        avg = avg.rename(columns = {'index':'Date-time'})
        fsave = HOME_DIR + AVG_DIR + file_prefix + fn1
        avg.to_csv(fsave,sep=";",float_format='%.1f',index=False)
    except Exception as e:
        logging.warning("An error occurred in making data averages: " + str(e))
    return fsave
#######################################################
#######################################################

## devices scanning: this routine search devices and the ports where they are plugged into.
## Then it creates the connections
def device_scanning(conn_dev,dev,sk1,ser1,flag):
    global fault
    global blink
    #resetting the fault alarm
    fault = False
    #making the yellow led rapidly blinking
    blink = True
    _thread.start_new_thread(led_blinking,())
    # number of magnitudes to acquire
    num_mag = 0
    for cn in conn_dev:
        cn.terminate()
        del cn
    conn_dev = []
    for dve in dev:
        conn_type = dve.getConnectionType()
        if (conn_type != USB_CONNECTION_TYPE) and (conn_type != SERIAL_CONNECTION_TYPE):
            conn_par = dve.getConnectionParams()
            for address in conn_par:
                if conn_type == I2C_CONNECTION_TYPE:
                    address_to_check = hex(address)
                else:
                    address_to_check = address
                if flag != 0:
                    send_output("\nSearching for " + dve.getIdentity() + " on " + address_to_check + "\n",sk1,ser1)
                else:
                    print ("\nSearching for " + dve.getIdentity() + " on " + address_to_check)
                    logging.warning("Searching for " + dve.getIdentity() + " on " + address_to_check)
                conn_dev.append(copy.deepcopy(dve))
                if conn_dev[-1].connect(address) == 1:
                    sens = conn_dev[-1].getSensors()
                    meas = conn_dev[-1].sample()
                    num_sens = sens.split(';')
                    num_meas = meas.split(';')
                    if len(num_sens) != len(num_meas):
                        conn_dev[-1].terminate()
                        del conn_dev[-1]
                        continue
                    if flag != 0:
                        send_output("FOUND " + conn_dev[-1].getIdentity() + "\n",sk1,ser1)
                        send_output("measures: " + conn_dev[-1].getSensors() + "\n",sk1,ser1)
                    else:
                        print ("FOUND " + conn_dev[-1].getIdentity())
                        print ("measures: " + conn_dev[-1].getSensors())
                        logging.warning("FOUND " + conn_dev[-1].getIdentity() + "; " + "measures: " + conn_dev[-1].getSensors())
                    #updating the number of magnitudes to acquire
                    num_mag = num_mag + len(num_sens)
                    #updating device identity for multi-copies purposes
                    original_identity = conn_dev[-1].getIdentity()
                    conn_dev[-1].setIdentity(original_identity + "-" + address_to_check)
                else:
                    if flag != 0:
                        send_output(dve.getIdentity() + " NOT FOUND\n",sk1,ser1)           
                    else:
                        print (dve.getIdentity() + " NOT FOUND")
                        logging.warning(dve.getIdentity() + " NOT FOUND")
                    del conn_dev[-1]
                    continue
    ports = list(serial.tools.list_ports.comports())
    for prt in ports:
        for dv in dev:
            conn_type = dv.getConnectionType()
            if (conn_type == USB_CONNECTION_TYPE) or (conn_type == SERIAL_CONNECTION_TYPE):
                if flag != 0:
                    send_output("\nSearching for " + dv.getIdentity() + " on " + prt[0] + " port\n",sk1,ser1)
                else:
                    print ("\nSearching for " + dv.getIdentity() + " on " + prt[0] + " port")
                    logging.warning("Searching for " + dv.getIdentity() + " on " + prt[0] + " port")
                conn_dev.append(copy.deepcopy(dv))
                if conn_dev[-1].connect(prt[0]) == 1:
                    sens = conn_dev[-1].getSensors()
                    meas = conn_dev[-1].sample()
                    num_sens = sens.split(';')
                    num_meas = meas.split(';')
                    if len(num_sens) != len(num_meas):
                        conn_dev[-1].terminate()
                        del conn_dev[-1]
                        continue
                    if flag != 0:
                        send_output("FOUND " + conn_dev[-1].getIdentity() + "\n",sk1,ser1)
                        send_output("measures: " + conn_dev[-1].getSensors() + "\n",sk1,ser1)
                    else:
                        print ("FOUND " + conn_dev[-1].getIdentity())
                        print ("measures: " + conn_dev[-1].getSensors())
                        logging.warning("FOUND " + conn_dev[-1].getIdentity() + "; " + "measures: " + conn_dev[-1].getSensors())
                    #updating the number of magnitudes to acquire
                    num_mag = num_mag + len(num_sens)
                    #updating device identity for multi-copies purposes
                    original_identity = conn_dev[-1].getIdentity()
                    conn_dev[-1].setIdentity(original_identity + "-" + prt[0])
                    break
                else:
                    if flag != 0:
                        send_output(dv.getIdentity() + " NOT FOUND\n",sk1,ser1)           
                    else:
                        print (dv.getIdentity() + " NOT FOUND")
                        logging.warning(dv.getIdentity() + " NOT FOUND")
                    del conn_dev[-1]
            else:
                continue
    if len(conn_dev) == 0:
        if flag != 0:
            send_output("\nNo device connected to SentinAir\n",sk1,ser1)   
        else:
            print("\nNo device connected to SentinAir")
            logging.warning("No device connected to SentinAir")
    blink = False
    return conn_dev,num_mag

## getting the devices informations: identity, measurements units, current measurements
def check_devices(conn_dev,sk1,ser1):
    if len(conn_dev) == 0:
        send_output("\nNo device connected to SentinAir\n",sk1,ser1)
    else:
        send_output("\nDevices connected:\n",sk1,ser1)
        for cnd in conn_dev:
            send_output(cnd.getIdentity() + "\n",sk1,ser1)
            send_output(cnd.getSensors() + "\n",sk1,ser1)
            send_output(cnd.sample() + "\n",sk1,ser1)

def close_file(f):
    try:
        f.close()
        return 0
    except:
        return 10

## formats the measures string to log and data logging
def measure_logging(f,towrite):
    try:
        towrite1 = towrite.rstrip(";")
        f.write(towrite1 + "\n")
        f.flush()
        return 0
    except:
        return 1

## builds the record to store in the file data by gathering measure from all the devices connected
def make_record(conn_dvc):
    view = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
    rec = time.strftime("%Y-%m-%d %H:%M:%S") + ';'
    errs = 0
    for cnd in conn_dvc:
        view = view + cnd.getIdentity() + "\n"
        head = cnd.getSensors()
        meas = cnd.sample()  
        index = 0
        hh = head.split(';')
        mm = meas.split(';')
        try:
            while index < len(hh):
                view = view + hh[index] + ": " + mm[index] + "\n"
                index = index + 1
        except:
            rec = "ERROR 21: bad data string from " + cnd.getIdentity()
            logging.warning(rec)
            view = rec
            errs = 21
            return rec,view,errs
        rec = rec + meas + ';'
    return rec,view,errs

## measurement session initalization operations
def init_session(conn_dvc,rt):
    try:
        ff = open("./status.sentinair","w")
        ff.write(str(rt) + "\n")
        ff.close
    except:
        pass
    try:
        fh = None
        temp = time.strftime("%Y-%m-%d_%H-%M-%S")
        try:
            f = open("/etc/hostname","r")
            machine_name = f.readline().rstrip("\r\n")
        except:
            machine_name = ""
        filename = HOME_DIR + DATA_DIR + machine_name + '_' + temp + ".txt"
        fh = open(filename,  'w')
        recstr = "Date-time;"
        for cn in conn_dvc:
            idstr = cn.getIdentity()
            headstr = cn.getSensors()
            sensstr = headstr.split(';')
            for ss in sensstr:
                recstr = recstr + idstr + '_' + ss + ';'
        recstr1 = recstr.rstrip(";")#new
        recstr1 = recstr1 + "\n"
        fh.write(recstr1)
        fh.flush()
        return 0,fh,filename,recstr1.rstrip("\n")
    except Exception as e:
        fh = None
        filename = machine_name + '_' + temp + ".txt"
        logging.warning("Monitoring init failed! ",exc_info=True)
        return 1,fh,filename,""

## measurement session closing operations
def session_closing(sk,fh1,errl):
    global rate
    global measure
    global fault
    rate = 0
    measure = NO_MEAS
    GPIO.output(13,GPIO.LOW)
    if errl > 0:
        fault = True
        _thread.start_new_thread(fault_alarm,())
    else:
        fault = False
    if fh1 is None:
        return
    res = close_file(fh1)
    if res == 0:
        send_data(sk,"File " + fh1.name + " closed")
        logging.warning("File " + fh1.name + " closed")
    else:
        send_data(sk,"Impossible closing " + fh1.name + "\n\nsession stopped with error")
        logging.warning("Impossible closing " + fh1.name + ". session stopped with error")


## measurement session management routine
def capture(sk,conn_dvc):
    global rate
    global measure
    global curfile
    global fault
    errorLevel = 0
    ##############################
    fault = False
    try:
        errorLevel, fh, curfile, head = init_session(conn_dvc,rate)## builds the measurements record
    except Exception as e:
        logging.warning(INIT_CAPT_ERR_LOG_MSG,exc_info=True)
    if errorLevel > 0:
        measure = NO_MEAS
        send_data(sk,DATA_FILE_OPENING_ERR) 
        logging.warning(DATA_FILE_OPENING_ERR)
        try:
            GPIO.output(13,GPIO.LOW)
            fault = True
            _thread.start_new_thread(fault_alarm,())
        except Exception as e:
            logging.warning(INIT_CAPT_GPIO_ERR_LOG_MSG_2,exc_info=True)
        session_closing(sk,fh,errorLevel) 
        return
    try:
        tolog, measure , errorLevel = make_record(conn_dvc)## builds the measurements record
    except Exception as e:
        logging.warning(INIT_CAPT_MAKE_ERR_LOG_MSG,exc_info=True)
        errorLevel = 22
    if errorLevel > 0:
        send_data(sk,tolog + MEAS_STOP_ERR_MSG)
        logging.warning(tolog + MEAS_STOP_ERR_MSG)
        session_closing(sk,fh,errorLevel)       
        return
    send_data(sk,measure)
    adesso = time.time()
    res = measure_logging(fh,tolog)
    _thread.start_new_thread(plotter,(curfile,))
    while(rate!=0):## loop where devices are read if it is the time
        GPIO.output(13,GPIO.HIGH)
        dopo = time.time()
        diff = int(dopo-adesso)
        if(diff>=rate):## now it is the time to read the devices, gather and treat the data
            adesso = time.time()
            try:
                tolog, measure , errorLevel = make_record(conn_dvc)## build the record of measurements to store
            except Exception as e:
                logging.warning(MAKE_ERR_LOG_MSG,exc_info=True)            
            if errorLevel > 0:
                send_data(sk,tolog + MEAS_STOP_ERR_MSG)
                logging.warning(tolog + MEAS_STOP_ERR_MSG)
                session_closing(sk,fh,errorLevel) 
                return
            ################### no error occurred
            if rate != 0:
                send_data(sk,measure)
                res = measure_logging(fh,tolog)## logs the measurements in the correct format
                if errorLevel > 0:
                    send_data(sk,MEAS_STOP_ERR_MSG)
                    logging.warning(MEAS_STOP_ERR_MSG)
                    session_closing(sk,fh,errorLevel)       
                    return   
            ##########################################
    ####  closing opertions
    session_closing(sk,fh,errorLevel)

## function to manage the stop button pressed event
def my_callback(channel):
    global rate
    time.sleep(4)
    if GPIO.input(17):
        return
    try:
        rate = 0
        GPIO.output(13,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(13,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(13,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(13,GPIO.HIGH)
        logging.warning(SHUTDOWN_BUTTON_PRESSED)
        os.popen("sudo shutdown -h now")
    except Exception as e:
        print ("Shutdown system failed!")

## function to make blink the yellow check light
def led_blinking():
    global blink
    while blink:
        GPIO.output(13,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(13,GPIO.LOW)
        time.sleep(0.2)
    GPIO.output(13,GPIO.LOW)

## function to make blink the red check light for fault indication
def fault_alarm():
    global fault
    while fault:
        GPIO.output(26,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(26,GPIO.LOW)
        time.sleep(0.2)
    GPIO.output(26,GPIO.HIGH)

## function to get started udp socket communications with user interfaces
def init_consolle():
    s = None
    sock = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)## creation of the socket for system reponses 
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((UDP_HOST_BINDING,UDP_SERVICE_PORT))
    except Exception as e:
        print(str(e))
        print (UDP_CLI_PORT_ERR_MSG)
        logging.warning(UDP_CLI_PORT_ERR_LOG_MSG ,exc_info=True)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)## creation of socket for data output
        sock.settimeout(10)
    except Exception as e:
        print (DATA_PORT_OPEN_ERR_MSG)
        print(str(e))
        logging.warning(DATA_PORT_OPEN_ERR_LOG_MSG,exc_info=True)
    return s,sock

## function to get users commands from udp socket connected with the user interfaces
def get_input(sk):
    try:
        data, addr = sk.recvfrom(BUFSIZE)
        return data.decode(),addr
    except Exception as e:
        data = __ERROR
        addr = None
        logging.warning(CMD_IN_ERR_LOG_MSG,exc_info=True)


## function to send system responses through udp socket connected with the user interfaces
def send_output(str1,sk,sr):
    try:
        sent = sk.sendto(str1.encode(),sr)
        time.sleep(0.2)
    except Exception as e:
        logging.warning(CMD_OUT_ERR_LOG_MSG,exc_info=True)


## function to send data through udp socket connected with the user interfaces
def send_data(sk,data):
    try:
        sent = sk.sendto(data.encode(),DATA_ADDRESS)
        time.sleep(0.2)
    except:
        logging.warning(DATA_SENDING_ERR_LOG_MSG,exc_info=True)


## function to check if a mail account exists
def mail_account_check(maf):
    mail = 0
    pwd = 0
    smtp = 0
    imap = 0
    try:
        f = open(maf,"r")
        lines = f.readlines()
        for ll in lines:
            if ll.find("MAIL_ADDRESS")==0:
                ma = ll.split('"')
                if ma[1].find("@") > 0:
                    mail = 1
            if ll.find("MAIL_PWD")==0:
                pw = ll.split('"')
                if pw[1]!= "":
                    pwd = 1
            if ll.find("SMTP_SERVER")==0:
                sm = ll.split('"')
                if sm[1]!= "":
                    smtp = 1            
            if ll.find("IMAP_SERVER")==0:
                im = ll.split('"')
                if im[1]!= "":
                    imap = 1
        if (mail == 1) and (pwd == 1) and (smtp == 1) and (imap == 1):
            return 0
        else:
            logging.warning(MAIL_CONFIG_NULL_LOG_MSG)
            print(MAIL_CONFIG_NULL)
            return 1
    except Exception as e:
        logging.warning(MAIL_CONFIG_NULL_LOG_MSG)
        print(MAIL_CONFIG_NULL)
        return 1
    


#### MAIN #######
global rate
global blink
global fault
global machine_name
global ssock
global user
global passwd
global encstr
rate = 0
fault = False
srv = None
measure = NO_MEAS


############# current PID info ############
##print("CURRENT PID:")
##print(str(os.getpid()))
###########################################


try:
    print (INIT_MSG)
    logging.basicConfig(filename=HOME_DIR + LOG_DIR + LOG_FILENAME,level=logging.WARNING,format='%(asctime)s - %(message)s',datefmt='%d/%m/%Y_%H:%M:%S')
    logging.warning(INIT_LOG_MSG)
except:
    print (INIT_LOG_FILE_ERROR)
    ff = open("errors.txt","w")
    ff.write(str(datetime.now()) + "\n" + INIT_LOG_FILE_ERROR)
    ff.close()
    sys.exit(0)

### retreiving the device name to display in the web page
try:
    f = open("/etc/hostname","r")
    machine_name = f.readline().rstrip("\r\n")
    f.close()
except:
    machine_name = ""

### reading the user and pass for restricted server area
try:
    f = open("pass","rb")
    encstr = f.read().decode('ascii')
    f.close()
    base64_bytes = base64.b64decode(encstr)
    idpass = base64_bytes.decode('ascii')
    account = idpass.split(":")
    user = account[0]
    passwd = account[1]
except:
    user = "sentinair"
    passwd = "sentinair1"
    encstr = "c2VudGluYWlyOnNlbnRpbmFpcjE="

### setting up led check lights and stop button
try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.OUT)#red
    #GPIO.setup(19,GPIO.OUT)#green
    GPIO.setup(13,GPIO.OUT)#yellow
    GPIO.output(26,GPIO.HIGH)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback, bouncetime=600)
except Exception as e:
    logging.warning(INIT_GPIO_ERR_LOG_MSG,exc_info=True)
    print (INIT_GPIO_ERR_MSG)

### starting user interface cli services
sock,skdata = init_consolle()
if sock == None:
    logging.warning("Init command line interface failed!")


### setting up web server related services
try:
    ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssock.settimeout(90)
    httpd = http.server.HTTPServer(('', 80), Handler)
    t = threading.Thread(target=httpd.serve_forever)
    t.setDaemon(True)
    t.start()
except Exception as e:
    logging.warning(INIT_WEB_SERVER_SERVICES,exc_info=True)
    print ("\n" + INIT_WEB_SERVER_SERVICES + "\n")

#### device connected scanning
number_devices = 0
connected_devices,number_devices = device_scanning(connected_devices,installed_devices,sock,srv,0)
# calculating the MINIMUM_SAMPLING_RATE. It depends on the number of devices connected
if number_devices < 12:
    MINIMUM_SAMPLING_RATE = 30
if (number_devices > 11) and (number_devices < 22):
    MINIMUM_SAMPLING_RATE = 60
if (number_devices > 21) and (number_devices < 33):
    MINIMUM_SAMPLING_RATE = 90
if (number_devices > 32):
    MINIMUM_SAMPLING_RATE = 120

### resuming sentinair status
try:
    ff = open("./status.sentinair","r")
    strval = ff.readline().rstrip("\n")
    ff.close()
except:
    rate = 0
try:
    val = int(strval)
except:
    val = 0
if (val < MINIMUM_SAMPLING_RATE) or (len(connected_devices)==0):
    rate = 0
else:
    rate = val
    if srv != None:
        strout1 = "\r\nSession started at " + strval + " sec. rate "
        send_output(strout1,sock,srv)
    strlog1 = "Session started at " + strval + " sec. rate "
    logging.warning(strlog1)
    _thread.start_new_thread(capture,(skdata,connected_devices))

if mail_account_check(MAIL_CONFIG_FILE) == 0:
    #### starting imap-smtp interface
    try:
        os.system("sudo python3 " + IMAP_SMTP_FILE + "&")
    except Exception as e:
        logging.warning("Imap-smtp interface starting failed:",exc_info=True)


#### starting operations finished 
print (SYS_READY)
logging.warning(SYS_READY_LOG_MSG)

### infinite loop to get users commands and return system responses
while 1:
    try:
        command,srv = get_input(sock)
    except:
        command = __ERROR
    if (command!=__ERROR):
        if command == 's':## scan devices command arrived
            if (rate ==0):
                connected_devices,number_devices = device_scanning(connected_devices,installed_devices,sock,srv,1)
                send_output(END_STR,sock,srv)
            else:
                send_output(ERRS_STR + END_STR,sock,srv)
            continue
        elif command == 'b':## stop measurement session command arrived
            if rate != 0:
                rate = 0
                send_output("Measurement session stopped  \n" + END_STR,sock,srv)
                logging.warning('Measurement session stopped')
                try:
                    ff1 = open(HOME_DIR + "status.sentinair","w")
                    strval = ff1.write("0\n")
                    ff1.close()
                except Exception as e:
                    logging.warning(STATUS_FILE_ERR_LOG_MSG,exc_info=True)
                    pass
            else:
                send_output("No measurement session to stop!\n" + END_STR,sock,srv)
            continue
        elif command == 'c':## check devices command arrived
            if rate == 0:
                check_devices(connected_devices,sock,srv)
                send_output(END_STR,sock,srv)
            else:
                send_output(ERRC_STR + END_STR,sock,srv)
            continue
        elif command == 'h':## brief user manual request command arrived
            send_output(USAGE_STR + END_STR,sock,srv)
            continue
        elif command == 'i':## information about system status command arrived
            if rate == 0:
                msg1 = "No monitoring session ongoing"
                send_output(msg1,sock,srv)
                check_devices(connected_devices,sock,srv)
                send_output(END_STR,sock,srv)
            else:
                msg1 = "Monitoring underway at " + str(rate) + "sec. rate\nData storage file: " +\
                       curfile + "\nLast devices readout:\n" + measure
                send_output(msg1 + END_STR,sock,srv)
            continue
        elif (command.find('s') == 0) and (len(command)>1):# measurement session starting command arrived
            if (len(connected_devices) > 0):
                if rate==0:
                    par = command.split(',')
                    try:
                        rt = int(par[1])
                        # calculating the MINIMUM_SAMPLING_RATE. It depends on the number of devices connected
                        if number_devices < 12:
                            MINIMUM_SAMPLING_RATE = 30
                        if (number_devices > 11) and (number_devices < 22):
                            MINIMUM_SAMPLING_RATE = 60
                        if (number_devices > 21) and (number_devices < 33):
                            MINIMUM_SAMPLING_RATE = 90
                        if (number_devices > 32):
                            MINIMUM_SAMPLING_RATE = 120
                        if rt >= MINIMUM_SAMPLING_RATE:
                            rate = rt
                            strout = "\r\nMonitoring started at " + par[1] + " sec. rate "
                            send_output(strout + END_STR,sock,srv)
                            strlog = "Monitoring started at " + par[1] + " sec. rate "
                            logging.warning(strlog)
                            _thread.start_new_thread(capture,(skdata,connected_devices))
                        else:
                            str1 = "Impossible to start a new monitoring session:\n"
                            str2 = "please, select a sampling rate greater than " + str(MINIMUM_SAMPLING_RATE) + " seconds or equal!"
                            strout = str1 + str2 + END_STR
                            send_output(strout,sock,srv)
                    except Exception as e:
                        strout = "ERROR: " + par[1] + " is not a valid number" + END_STR
                        send_output(strout,sock,srv)
                else:
                    send_output(ERRS_STR + END_STR,sock,srv)
            else:
                send_output(ERRS_STR_1 + END_STR,sock,srv)
            continue
        else:
            if (rate == 0):
                send_output(INV_CMD + END_STR,sock,srv)
            else:
                send_output(ERRS_STR + END_STR,sock,srv)
