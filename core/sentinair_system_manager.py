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

installed_devices = []
#v72m has been installed in SentinAir on 2020-07-31_04-48-53
# do not remove or modify the next three lines below!!!
from devices.v72m import V72m
v72m_obj = V72m()
installed_devices.append(v72m_obj)
#multisensor_board has been installed in SentinAir on 2020-07-31_01-10-48
# do not remove or modify the next three lines below!!!
from devices.multisensor_board import Multisensor_board
multisensor_board_obj = Multisensor_board()
installed_devices.append(multisensor_board_obj)
#irca1 has been installed in SentinAir on 2020-07-27_10-06-03
from devices.irca1 import Irca1
irca1_obj = Irca1()
installed_devices.append(irca1_obj)
#go3 has been installed in SentinAir on 2020-05-29_15-41-24
from devices.go3 import Go3
go3_obj = Go3()
installed_devices.append(go3_obj)
#af22 has been installed in SentinAir on 2020-05-27_13-19-26
from devices.af22 import Af22
af22_obj = Af22()
installed_devices.append(af22_obj)
#ac32 has been installed in SentinAir on 2020-05-20_15-22-54
from devices.ac32 import Ac32
ac32_obj = Ac32()
installed_devices.append(ac32_obj)
#co12m has been installed in SentinAir on 2020-05-20_15-22-39
# do not remove or modify the next three lines below!!!
from devices.co12m import Co12m
co12m_obj = Co12m()
installed_devices.append(co12m_obj)
# do not remove or modify the next three lines below!!!
#lcss_adapter has been installed in SentinAir on 2020-05-20_15-22-17
# do not remove or modify the next three lines below!!!
from devices.lcss_adapter import Lcss_adapter
lcss_adapter_obj = Lcss_adapter()
installed_devices.append(lcss_adapter_obj)
# do not remove or modify the next three lines below!!!
#nox405 has been installed in SentinAir on 2020-05-20_15-21-55
# do not remove or modify the next three lines below!!!
from devices.nox405 import Nox405
nox405_obj = Nox405()
installed_devices.append(nox405_obj)
#o342 has been installed in SentinAir on 2020-05-20_15-21-48
# do not remove or modify the next three lines below!!!
from devices.o342 import O342
o342_obj = O342()
installed_devices.append(o342_obj)
#pms3003 has been installed in SentinAir on 2020-05-20_15-21-41
# do not remove or modify the next three lines below!!!
from devices.pms3003 import Pms3003
pms3003_obj = Pms3003()
installed_devices.append(pms3003_obj)
# do not remove or modify the next three lines below!!!
#multisensore has been installed in SentinAir on 2020-05-09_22-23-17
# do not remove or modify the next three lines below!!!

import copy
import serial.tools.list_ports
import serial
import time
import _thread
import logging
import RPi.GPIO as GPIO
from socket import *
import sys
from datetime import datetime
import os
#graphic management libraries
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
#end

#connected devices are stored here
connected_devices = []

#sentinair files paths
DEFAULT_DIR = "/home/pi/sentinair"
DATA_DIR = "/var/www/html/data"
IMG_DIR = "/var/www/html/img"
LOG_FILENAME = '/var/www/html/log/sentinair-log.txt'
IMAP_SMTP_FILE = "/home/pi/sentinair/imap-smtp-interface.py"
MAIL_CONFIG_FILE = "/home/pi/sentinair/mail-config.sentinair"

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
UDP_CLI_PORT_ERR_LOG_MSG = 'Unable to start SentinAir command line user interface: udp port not opening!'
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
INIT_CAPT_MAKE_ERR_LOG_MSG = 'Error on make_recoed in init capture:'
MAKE_ERR_LOG_MSG = 'Error on make_record capture:'
SYS_READY_LOG_MSG = 'SentinAir ready!'
AVG_INIT_ERR_LOG_MSG = 'Error in calculating means on init:'
AVG_HOUR_ERR_LOG_MSG = 'Error in calculating hourly means:'
AVG_DAY_ERR_LOG_MSG = 'Error in calculating daily means:'
DATA_PORT_OPEN_ERR_LOG_MSG = "Udp data port opening failed"
MAIL_CONFIG_NULL_LOG_MSG = "E-mail account is not present: the imap-smtp interface will not start"

INIT_MSG = "\n\n" + INIT_LOG_MSG + "\n"
UDP_CLI_PORT_ERR_MSG = "\n" + UDP_CLI_PORT_ERR_LOG_MSG + "\n"
INIT_GPIO_ERR_MSG = "\n" + INIT_GPIO_ERR_LOG_MSG + '\n'
UDP_CLI_PORT_ERR_MSG = "\n" + UDP_CLI_PORT_ERR_LOG_MSG + "\n"
DATA_SERVER_ERR_MSG = "\n" + DATA_SERVER_ERR_LOG_MSG + "\n"
DATA_SERVER_PORT_ERR_MSG = "\n" + DATA_SERVER_PORT_ERR_LOG_MSG + "\n"
DATA_SENDING_ERR_MSG = "\n" + DATA_SENDING_ERR_LOG_MSG + "\n"
DATA_FILE_OPENING_ERR = "Impossible opening storage data file. Measurement sesssion stopped with error"
MEAS_STOP_ERR_MSG = "Measurement session stopped with error"
SYS_READY = "\n" + SYS_READY_LOG_MSG + "\n"
INV_CMD = "Command not valid!\n"
DATA_PORT_OPEN_ERR_MSG = DATA_PORT_OPEN_ERR_LOG_MSG + "\n"
MAIL_CONFIG_NULL = "\nE-mail account is not present: the imap-smtp interface will not start\n"


ERRS_STR = "Impossible to execute the command:\n" +\
           "sampling session ongoing,\n" + "if you want to execute it\n" +\
           "first press 'b' to stop the session!\n"
ERRC_STR = "Impossible to execute the command:\n" +\
           "sampling session ongoing,\n" + "if you want to check on devices\n" +\
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

#system settings
MINIMUM_SAMPLING_RATE = 30
UDP_SERVICE_PORT = 16670
DATA_PORT = 24504
DATA_ADDRESS = ('localhost', DATA_PORT)
BUFSIZE = 1024


##### GRAPHIC
##### routine for plots generation
def plotter(heads):
    global rate
    global curfile
    global datacols
    global datacolsh
    global datacolsd
    nowlen = 0
    prevlen = 0
    nowlenh = 0
    prevlenh = 0
    nowlend = 0
    prevlend = 0
    fileh1 = curfile.rstrip(".txt")
    fileh = fileh1 + "_hourlymeans.txt"
    filed = fileh1 + "_dailymeans.txt"    
    while(rate!=0):
        nowlen = len(datacols[0])
        if (nowlen > 1) and (prevlen != nowlen):
            plot_file(curfile,heads)
            if rate == 0:
                datacols = []
                return
        prevlen = nowlen
        #hourlymean
        nowlenh = len(datacolsh[0])
        if (nowlenh > 1) and (prevlenh != nowlenh):
            plot_file_h(fileh,heads)
            if rate == 0:
                datacolsh = []
                return
        prevlenh = nowlenh
        #dailymean
        nowlend = len(datacolsd[0])
        if (nowlend > 1) and (prevlend != nowlend):
            plot_file_d(filed,heads)
            if rate == 0:
                datacolsd = []
                return
        prevlend = nowlend

#routine for plotting data of the measurements file
def plot_file(filename,header):
    global datacols
    global rate
    fn1 = filename.replace(DATA_DIR + "/",'')
    fn = fn1.rstrip("txt")
    j = 0
    for cols in header:
        if j == 0:
            j=j+1
            continue
        try:
            xm2 = [datetime.strptime(d,"%d/%m/%Y_%H:%M:%S") for d in datacols[0]]
            xm = mpl.dates.date2num(xm2)
            fig = plt.figure()
            graph = fig.add_subplot(111)
            red_patch = mpatches.Patch(color='red', label=header[j])
            graph.legend(handles=[red_patch])
            hfmt = mpl.dates.DateFormatter("%d/%m/%Y_%H:%M:%S")
            graph.xaxis.set_major_formatter(hfmt)
            if len(datacols[j]) > len(xm):
                df = len(datacols[j])-len(xm)
                yp = datacols[j][:-df]
            if len(xm) > len(datacols[j]):
                df = len(xm)- len(datacols[j])
                xm = xm[:-df]
            if len(datacols[j]) == len(xm):
                yp = datacols[j]
            if rate == 0:
                datacols = []
                plt.close('all')
                return
            graph.plot(xm,yp,'r')
            plt.setp(graph.get_xticklabels(), rotation=30, ha="right")
            ln1 = len(xm)
            if ln1<10:
                graph.xaxis.set_major_locator(plt.LinearLocator(numticks=ln1))
                graph.yaxis.set_major_locator(plt.LinearLocator(numticks=ln1))
            else:
                graph.xaxis.set_major_locator(plt.MaxNLocator(10))
                graph.yaxis.set_major_locator(plt.MaxNLocator(10))
            text = graph.annotate("Plotted by Sentinair device\n developed by\n Dr. Domenico Suriano 2019",\
                                  xy=(.3,.7),xycoords='figure fraction',rotation=-30,size=16,alpha=0.2)
            graph.set_xlabel('Date_time')
            graph.grid(True)
            head = header[j].split("_")
        except Exception as e:
            logging.warning("Error in plotting data:\r\n",exc_info=True)
            return
        try:
            ylabel = head[-1]
        except:
            ylabel = header[j]
        try:
            graph.set_ylabel(ylabel)
            header[j] = header[j].replace('%','')
            header[j] = header[j].replace('/','')
            imgdir = IMG_DIR.rstrip("/")
            fig.savefig(imgdir + "/" + fn + header[j] + ".png",dpi=80,format='png',bbox_inches='tight')
            plt.close('all')
        except Exception as e:
            logging.warning("Error in saving plot image data\r\n:",exc_info=True)
            return
        j=j+1

#routine for plotting data of the measurements file related to the hourly averages
def plot_file_h(filename,header):
    global datacolsh
    global rate
    fn1 = filename.lstrip(DATA_DIR)
    fn = fn1.rstrip("txt")
    j = 0
    for cols in header:
        if j == 0:
            j=j+1
            continue
        try:
            xm2 = [datetime.strptime(d,"%d/%m/%Y_%H") for d in datacolsh[0]]
            xm = mpl.dates.date2num(xm2)
            fig = plt.figure()
            graph = fig.add_subplot(111)
            red_patch = mpatches.Patch(color='red', label=header[j])
            graph.legend(handles=[red_patch])
            hfmt = mpl.dates.DateFormatter("%d/%m/%Y_%H")
            graph.xaxis.set_major_formatter(hfmt)
            if len(datacolsh[j]) > len(xm):
                df = len(datacolsh[j])-len(xm)
                yp = datacolsh[j][:-df]
            if len(xm) > len(datacolsh[j]):
                df = len(xm)- len(datacolsh[j])
                xm = xm[:-df]
            if len(datacolsh[j]) == len(xm):
                yp = datacolsh[j]
            if rate == 0:
                datacolsh = []
                plt.close('all')
                return
            graph.plot(xm,yp,'r')
            plt.setp(graph.get_xticklabels(), rotation=30, ha="right")
            ln1 = len(xm)
            if ln1<10:
                graph.xaxis.set_major_locator(plt.LinearLocator(numticks=ln1))
                graph.yaxis.set_major_locator(plt.LinearLocator(numticks=ln1))
            else:
                graph.xaxis.set_major_locator(plt.MaxNLocator(10))
                graph.yaxis.set_major_locator(plt.MaxNLocator(10))
            text = graph.annotate("Plotted by Sentinair device\n developed by\n Dr. Domenico Suriano 2019",\
                                  xy=(.3,.7),xycoords='figure fraction',rotation=-30,size=16,alpha=0.2)
            graph.set_xlabel('Date_time')
            graph.grid(True)
            head = header[j].split("_")
        except Exception as e:
            logging.warning("Error in plotting hourly mean data:\r\n" ,exc_info=True)
            return
        try:
            ylabel = head[-1]
        except:
            ylabel = header[j]
        try:
            graph.set_ylabel(ylabel)
            header[j] = header[j].replace('%','')
            header[j] = header[j].replace('/','')
            imgdir = IMG_DIR.rstrip("/")
            fig.savefig(imgdir + "/" + fn + header[j] + ".png",dpi=80,format='png',bbox_inches='tight')
            plt.close('all')
        except Exception as e:
            logging.warning("Error in saving hourly means data image: ",exc_info=True)
            return
        j=j+1

#routine for plotting data of the measurements file related to the daily averages
def plot_file_d(filename,header):
    global datacolsd
    global rate
    fn1 = filename.lstrip(DATA_DIR)
    fn = fn1.rstrip("txt")
    j = 0
    for cols in header:
        if j == 0:
            j=j+1
            continue
        try:
            xm2 = [datetime.strptime(d,"%d/%m/%Y") for d in datacolsd[0]]
            xm = mpl.dates.date2num(xm2)
            fig = plt.figure()
            graph = fig.add_subplot(111)
            red_patch = mpatches.Patch(color='red', label=header[j])
            graph.legend(handles=[red_patch])
            hfmt = mpl.dates.DateFormatter("%d/%m/%Y")
            graph.xaxis.set_major_formatter(hfmt)
            if len(datacolsd[j]) > len(xm):
                df = len(datacolsd[j])-len(xm)
                yp = datacolsd[j][:-df]
            if len(xm) > len(datacolsd[j]):
                df = len(xm)- len(datacolsd[j])
                xm = xm[:-df]
            if len(datacolsd[j]) == len(xm):
                yp = datacolsd[j]
            if rate == 0:
                datacolsd = []
                plt.close('all')
                return
            graph.plot(xm,yp,'r')
            plt.setp(graph.get_xticklabels(), rotation=30, ha="right")
            ln1 = len(xm)
            if ln1<10:
                graph.xaxis.set_major_locator(plt.LinearLocator(numticks=ln1))
                graph.yaxis.set_major_locator(plt.LinearLocator(numticks=ln1))
            else:
                graph.xaxis.set_major_locator(plt.MaxNLocator(10))
                graph.yaxis.set_major_locator(plt.MaxNLocator(10))
            text = graph.annotate("Plotted by Sentinair device\n developed by\n Dr. Domenico Suriano 2019",\
                                  xy=(.3,.7),xycoords='figure fraction',rotation=-30,size=16,alpha=0.2)
            graph.set_xlabel('Date')
            graph.grid(True)
            head = header[j].split("_")
        except Exception as e:
            logging.warning("Error in plotting daily mean data:\r\n",exc_info=True)
            return
        try:
            ylabel = head[-1]
        except:
            ylabel = header[j]
        try:
            graph.set_ylabel(ylabel)
            header[j] = header[j].replace('%','')
            header[j] = header[j].replace('/','')
            imgdir = IMG_DIR.rstrip("/")
            fig.savefig(imgdir + "/" + fn + header[j] + ".png",dpi=80,format='png',bbox_inches='tight')
            plt.close('all')
        except Exception as e:
            logging.warning("Error in saving daily means data image: ",exc_info=True)
            return
        j=j+1
###############################
        
##### AVERAGES CALCULATIONS ROUTINES
def get_decimal(ff):
    sstr = str(ff)
    if not '.' in sstr:
        return 0
    else:
        return len(sstr) - sstr.index('.')-1

### hourly averages calculation
def mean_hour(hrprev,hrnow,stephrn,smh,rec,fh,el):
    global datacolsh
    rec1 = rec.rstrip("\n")
    smh1 = smh.rstrip("\n")
    rec1p = rec1.split(';')
    smh1p = smh1.split(';')
    means = [None]*len(smh1p)
    smh1p[0] = str(hrprev)
    medie1 = time.strftime("%d/%m/%Y_") + "{:02d}".format(hrnow) + ';'
    sommenuove1 = smh1p[0] + ';'
    if hrprev == hrnow:
        stephrn = stephrn + 1
        ss = 1
        while ss < len(smh1p):
            fltsum = round(float(smh1p[ss]) + float(rec1p[ss]),get_decimal(rec1p[ss]))
            means[ss] = round(fltsum/float(stephrn),get_decimal(fltsum))
            medie1 = medie1 + str(means[ss]) + ';'
            sommenuove1 = sommenuove1 + str(fltsum) + ';'
            ss =  ss + 1
        medie = medie1.rstrip(';')
        sommenuove2 = sommenuove1.rstrip(';')
        sommenuove = sommenuove2  + "\n"
        errorLevel = 0
    else:
        ss = 1
        while ss < len(smh1p):
            fltsum = round(float(smh1p[ss]),get_decimal(smh1p[ss]))
            if stephrn == 0:
                stephrn = stephrn + 1
            means[ss] = round(fltsum/float(stephrn),get_decimal(fltsum))
            medie1 = medie1 + str(means[ss]) + ';'
            ss =  ss + 1
        medie = medie1.rstrip(';')
        ms1 = medie.rstrip("\n")
        ms = ms1.split(";")
        colnum = 0
        for m in ms:
            datacolsh[colnum].append(ms[colnum])
            colnum += 1
        errorLevel = measure_logging(fh,medie)
        stephrn = 0
        sommenuove = rec
        medie = rec
    hrprev = hrnow
    return hrprev,sommenuove,stephrn,medie,errorLevel


### daily averages calculation
def mean_daily(dprev,dnow,stepdn,smd,rec,fh,el):
    global datacolsd
    rec1 = rec.rstrip("\n")
    smd1 = smd.rstrip("\n")
    rec1p = rec1.split(';')
    smd1p = smd1.split(';')
    means = [None]*len(smd1p)
    smd1p[0] = str(dprev)
    medie1 = dprev + ';'
    sommenuove1 = smd1p[0] + ';'
    if dprev == dnow:
        stepdn = stepdn + 1
        ss = 1
        while ss < len(smd1p):
            fltsum = round(float(smd1p[ss]) + float(rec1p[ss]),get_decimal(rec1p[ss]))
            means[ss] = round(fltsum/float(stepdn),get_decimal(fltsum))
            medie1 = medie1 + str(means[ss]) + ';'
            sommenuove1 = sommenuove1 + str(fltsum) + ';'
            ss =  ss + 1
        medie = medie1.rstrip(';')
        sommenuove2 = sommenuove1.rstrip(';')
        sommenuove = sommenuove2  + "\n"
        errorLevel = 0
    else:
        ss = 1
        while ss < len(smd1p):
            fltsum = round(float(smd1p[ss]),get_decimal(smd1p[ss]))
            if stepdn == 0:
                stepdn = stepdn + 1
            means[ss] = round(fltsum/float(stepdn),get_decimal(fltsum))
            medie1 = medie1 + str(means[ss]) + ';'
            ss =  ss + 1
        medie = medie1.rstrip(';')
        ms1 = medie.rstrip("\n")
        ms = ms1.split(";")
        colnum = 0
        for m in ms:
            datacolsd[colnum].append(ms[colnum])
            colnum += 1
        errorLevel = measure_logging(fh,medie)
        stepdn = 0
        sommenuove = rec
        medie = rec
    dprev = dnow
    return dprev,sommenuove,stepdn,medie,errorLevel
###################################

## devices scanning: this routine search devices and the ports where they are plugged into.
## Then it creates the connections
def device_scanning(conn_dev,dev,sk1,ser1,flag):
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
            if flag != 0:
                send_output("\nSearching for " + dve.getDeviceType() + " on " + conn_par[0],sk1,ser1)
            else:
                print ("\nSearching for " + dve.getDeviceType() + " on " + conn_par[0])
            conn_dev.append(copy.deepcopy(dve))
            if conn_dev[-1].connect() == 1:
                sens = conn_dev[-1].getSensors()
                meas = conn_dev[-1].sample()
                num_sens = sens.split(';')
                num_meas = meas.split(';')
                if len(num_sens) != len(num_meas):
                    conn_dev[-1].terminate()
                    del conn_dev[-1]
                    continue
                if flag != 0:
                    send_output("FOUND " + conn_dev[-1].getIdentity(),sk1,ser1)
                    send_output("measures: " + conn_dev[-1].getSensors(),sk1,ser1)
                else:
                    print ("FOUND " + conn_dev[-1].getIdentity())
                    print ("measures: " + conn_dev[-1].getSensors())
                #updating the number of magnitudes to acquire
                num_mag = num_mag + len(num_sens)
            else:
                if flag != 0:
                    send_output(dve.getDeviceType() + " NOT FOUND",sk1,ser1)           
                else:
                    print (dve.getDeviceType() + " NOT FOUND")              
                del conn_dev[-1]
                continue
    ports = list(serial.tools.list_ports.comports())
    for prt in ports:
        for dv in dev:
            conn_type = dv.getConnectionType()
            if (conn_type == USB_CONNECTION_TYPE) or (conn_type == SERIAL_CONNECTION_TYPE):
                if flag != 0:
                    send_output("\nSearching for " + dv.getDeviceType() + " on " + prt[0] + " port",sk1,ser1)
                else:
                    print ("\nSearching for " + dv.getDeviceType() + " on " + prt[0] + " port")
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
                        send_output("FOUND " + conn_dev[-1].getIdentity(),sk1,ser1)
                        send_output("measures: " + conn_dev[-1].getSensors(),sk1,ser1)
                    else:
                        print ("FOUND " + conn_dev[-1].getIdentity())
                        print ("measures: " + conn_dev[-1].getSensors())
                    #updating the number of magnitudes to acquire
                    num_mag = num_mag + len(num_sens)
                    break
                else:
                    if flag != 0:
                        send_output(dv.getDeviceType() + " NOT FOUND",sk1,ser1)           
                    else:
                        print (dv.getDeviceType() + " NOT FOUND")
                    del conn_dev[-1]
            else:
                continue
    if len(conn_dev) == 0:
        if flag != 0:
            send_output("\nNo device connected to SentinAir",sk1,ser1)   
        else:
            print("\nNo device connected to SentinAir")
    return conn_dev,num_mag

## getting the devices informations: identity, measurements units, current measurements
def check_devices(conn_dev,sk1,ser1):
    if len(conn_dev) == 0:
        send_output("\nNo device connected to SentinAir",sk1,ser1)
    else:
        send_output("\nDevices connected:\n",sk1,ser1)
        for cnd in conn_dev:
            send_output(cnd.getIdentity(),sk1,ser1)
            send_output(cnd.getSensors(),sk1,ser1)
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
    view = time.strftime("%d/%m/%Y_%H:%M:%S") + "\n"
    rec = time.strftime("%d/%m/%Y_%H:%M:%S") + ';'
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
    sdir = DEFAULT_DIR.rstrip("/")
    ddir = DATA_DIR.rstrip("/")
    try:
        ff = open(sdir + "/" + "status.sentinair","w")
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
        filename = ddir + "/" + machine_name + '_' + temp + ".txt"
        filemh = ddir + "/" + machine_name + '_' + temp + "_hourlymeans.txt"
        filemd = ddir + "/" + machine_name + '_' + temp + "_dailymeans.txt"
        fh = open(filename,  'w')
        f_handle_hm = open(filemh,  'w')
        f_handle_dm = open(filemd,  'w')
        recstr = "Date/time;"
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
        f_handle_hm.write(recstr1)
        f_handle_hm.flush()
        f_handle_dm.write(recstr1)
        f_handle_dm.flush()
        return 0,fh,filename,f_handle_hm,f_handle_dm,recstr1.rstrip("\n")
    except:
        fh = None
        filename = ""
        return 1,fh,filename,f_handle_hm,f_handle_dm,Null

## measurement session closing operations
def session_closing(sk,fh1,fhmh1,fhmd1,errl):
    global rate
    global measure
    rate = 0
    measure = NO_MEAS
    res = close_file(fh1)
    GPIO.output(19,GPIO.LOW)
    if errl > 0:
        GPIO.output(13,GPIO.HIGH)        
    if res == 0:
        send_data(sk,"File " + fh1.name + " closed")
        logging.info("File " + fh1.name + " closed")
    else:
        send_data(sk,"Impossible closing " + fh1.name + "\n\nsession stopped with error")
        logging.warning("Impossible closing " + fh1.name + ". session stopped with error")
        GPIO.output(13,GPIO.HIGH)
    res = close_file(fhmh1)
    if res == 0:
        send_data(sk,"File " + fhmh1.name + " closed")
        logging.info("File " + fhmh1.name + " closed")
    else:
        send_data(sk,"Impossible closing " + fhmh1.name + "\n\nsession stopped with error")
        logging.warning("Impossible closing " + fhmh1.name + ". session stopped with error")
    res = close_file(fhmd1)
    if res == 0:
        send_data(sk,"File " + fhmd1.name + " closed")
        logging.info("File " + fhmd1.name + " closed")
    else:
        send_data(sk,"Impossible closing " + fhmd1.name + "\n\nsession stopped with error")
        logging.warning("Impossible closing " + fhmd1.name + ". session stopped with error")


## measurement session management routine
def capture(sk,conn_dvc):
    global rate
    global datacols
    global datacolsh
    global datacolsd
    global measure
    global curfile
    del datacols[:]
    del datacolsh[:]
    del datacolsd[:]
    errorLevel = 0
    ### averages related veriables
    sumhr = ""
    stephr = 0
    sumd = ""
    stepd = 0
    dayprev = time.strftime("%d/%m/%Y")
    hourprev = datetime.now().hour
    ##############################
    try:
        GPIO.output(13,GPIO.LOW)
    except Exception as e:
        logging.warning(INIT_CAPT_GPIO_ERR_LOG_MSG,exc_info=True)
    try:
        errorLevel, fh, curfile, fhmh, fhmd, head = init_session(conn_dvc,rate)## builds the measurements record
    except Exception as e:
        logging.warning(INIT_CAPT_ERR_LOG_MSG,exc_info=True)
    if errorLevel > 0:
        measure = NO_MEAS
        send_data(sk,DATA_FILE_OPENING_ERR) 
        logging.warning(DATA_FILE_OPENING_ERR)
        try:
            GPIO.output(13,GPIO.HIGH)
            GPIO.output(19,GPIO.LOW)
        except Exception as e:
            logging.warning(INIT_CAPT_GPIO_ERR_LOG_MSG_2,exc_info=True)
        session_closing(sk,fh,fhmh,fhmd,errorLevel) 
        return
    try:
        tolog, measure , errorLevel = make_record(conn_dvc)## builds the measurements record
    except Exception as e:
        logging.warning(INIT_CAPT_MAKE_ERR_LOG_MSG,exc_info=True)
        errorLevel = 22
    if errorLevel > 0:
        send_data(sk,tolog + MEAS_STOP_ERR_MSG)
        logging.warning(tolog + MEAS_STOP_ERR_MSG)
        session_closing(sk,fh,fhmh,fhmd,errorLevel)       
        return
    #### init averages calcultions
    ss = 1
    try:
        tolog1 = tolog.rstrip(';')
        recorditems = tolog1.split(';')
        sumhr1 = sumhr + recorditems[0] + ';'
        sumd1 = sumd + recorditems[0] + ';'
        while ss < len(recorditems):
            sumhr1 = sumhr1 + "0.0" + ';'
            sumd1 = sumd1 + "0.0" + ';'
            ss = ss + 1
        sumhr = sumhr1.rstrip(';')
        sumd = sumd1.rstrip(';')
        hournow = datetime.now().hour
        daynow = time.strftime("%d/%m/%Y")
        hourprev,sumhr,stephr,medieh,errorLevel1 = mean_hour(hourprev,hournow,stephr,sumhr,tolog1,fhmh,errorLevel)
        dayprev,sumd,stepd,medied,errorLevel2 = mean_daily(dayprev,daynow,stepd,sumd,tolog1,fhmd,errorLevel)
        errorLevel = errorLevel1 + errorLevel2
        #building sensor data matrix
        header = head.split(';')
        strmeas = tolog.rstrip(';')
        ms = strmeas.split(';')
    except Exception as e:
        logging.warning(AVG_INIT_ERR_LOG_MSG,exc_info=True)
        errorLevel = 3
    if errorLevel > 0:
        send_data(sk,MEAS_STOP_ERR_MSG)
        logging.warning(MEAS_STOP_ERR_MSG)
        session_closing(sk,fh,fhmh,fhmd,errorLevel)       
        return
    ## init variables for data plotting
    try:
        colnum = 0
        for cols in header:
            datacols.append([])
            datacolsh.append([])
            datacolsd.append([])
        for m in ms:
            datacols[colnum].append(ms[colnum])
            colnum += 1
        _thread.start_new_thread(plotter,(header,))##starting the thread in charge of plotting data
    except ValueError as ve:
        logging.warning("Error in building matrix to plot:",exc_info=True)
        pass
    except Exception as e:
        logging.warning("Error in building matrix to plot:",exc_info=True)
        pass    
    send_data(sk,measure)
    adesso = time.time()
    res = measure_logging(fh,tolog)
    while(rate!=0):## loop where devices are read if it is the time
        GPIO.output(19,GPIO.HIGH)
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
                session_closing(sk,fh,fhmh,fhmd,errorLevel) 
                return
            ################### no error occurred
            if rate != 0:
                send_data(sk,measure)
                res = measure_logging(fh,tolog)## logs the measurements in the correct format
                tolog1 = tolog.rstrip(';')
                #updating sensor data matrix
                strmeas = tolog.rstrip(';')
                ms = strmeas.split(';')
                colnum = 0
                try:
                    for m in ms:
                        datacols[colnum].append(ms[colnum])
                        colnum += 1
                except ValueError as ve:
                    logging.warning("Error in updating matrix to plot:",exc_info=True)
                    pass
                except Exception as e:
                    logging.warning("Error in updating matrix to plot:",exc_info=True)
                    pass
                #end
                hournow = datetime.now().hour
                try:
                    hourprev,sumhr,stephr,medieh,errorLevel1 = mean_hour(hourprev,hournow,stephr,sumhr,tolog1,fhmh,errorLevel)
                except Exception as e:
                    logging.warning(AVG_HOUR_ERR_LOG_MSG,exc_info=True)
                    errorLevel1 = 20
                daynow = time.strftime("%d/%m/%Y")
                try:
                    dayprev,sumd,stepd,medied,errorLevel2 = mean_daily(dayprev,daynow,stepd,sumd,tolog1,fhmd,errorLevel)
                except Exception as e:
                    logging.warning(AVG_DAY_ERR_LOG_MSG,exc_info=True)
                    errorLevel1 = 30
                errorLevel = errorLevel1 + errorLevel2
                if errorLevel > 0:
                    send_data(sk,MEAS_STOP_ERR_MSG)
                    logging.warning(MEAS_STOP_ERR_MSG)
                    session_closing(sk,fh,fhmh,fhmd,errorLevel)       
                    return   
            ##########################################
    ####  closing opertions
    session_closing(sk,fh,fhmh,fhmd,errorLevel)

## function to manage the stop button pressed event
def my_callback(channel):
    global rate
    time.sleep(4)
    if GPIO.input(17):
        return
    try:
        rate = 0
        GPIO.output(26,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(26,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(26,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(26,GPIO.HIGH)
        logging.warning(SHUTDOWN_BUTTON_PRESSED)
        os.popen("sudo shutdown -h now")
    except Exception as e:
        print ("Shutdown system failed!")

## function to make blink the red check light
def red_blinking():
    global blink
    while blink:
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
        s = socket(AF_INET, SOCK_DGRAM)## creation of the socket for system reponses 
        s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        s.bind(('localhost',UDP_SERVICE_PORT))
    except Exception as e:
        print (UDP_CLI_PORT_ERR_MSG)
        logging.warning(UDP_CLI_PORT_ERR_LOG_MSG ,exc_info=True)
    try:
        sock = socket(AF_INET, SOCK_DGRAM)## creation of socket for data output
        sock.settimeout(10)
    except Exception as e:
        print (DATA_PORT_OPEN_ERR_MSG)
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
        logging.warning(MAIL_CONFIG_NULL_LOG_MSG,exc_info=True)
        print(MAIL_CONFIG_NULL)
        return 1
    


#### MAIN #######
global rate
global blink
datacols = []
datacolsh = []
datacolsd = []
rate = 0
blink = True
srv = None
measure = NO_MEAS
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format='%(asctime)s - %(message)s',datefmt='%d/%m/%Y_%H:%M:%S')
logging.info(INIT_LOG_MSG)
print (INIT_MSG)

### setting up led check lights and stop button
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26,GPIO.OUT)#red
    GPIO.setup(19,GPIO.OUT)#green
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

#### device connected scanning
_thread.start_new_thread(red_blinking,())
number_devices = 0
connected_devices,number_devices = device_scanning(connected_devices,installed_devices,sock,srv,0)
blink = False
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
sdir = DEFAULT_DIR.rstrip("/")
try:
    ff = open(sdir + "/" + "status.sentinair","r")
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
    logging.info(strlog1)
    _thread.start_new_thread(capture,(skdata,connected_devices))

if mail_account_check(MAIL_CONFIG_FILE) == 0:
    #### starting imap-smtp interface
    try:
        os.system("sudo python3 " + IMAP_SMTP_FILE + "&")
    except Exception as e:
        logging.warning("Imap-smtp interface starting failed:",exc_info=True)


#### starting operations finished 
print (SYS_READY)
logging.info(SYS_READY_LOG_MSG)

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
                logging.info('Measurement session stopped')
                try:
                    ff1 = open(DEFAULT_DIR + "/" + "status.sentinair","w")
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
                msg1 = "No measurement session ongoing"
                send_output(msg1,sock,srv)
                check_devices(connected_devices,sock,srv)
                send_output(END_STR,sock,srv)
            else:
                msg1 = "Session underway at " + str(rate) + "sec. rate\nData storage file: " +\
                       curfile + ".\nLast devices readout:\n" + measure
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
                            strout = "\r\nSession started at " + par[1] + " sec. rate "
                            send_output(strout + END_STR,sock,srv)
                            strlog = "Session started at " + par[1] + " sec. rate "
                            logging.info(strlog)
                            _thread.start_new_thread(capture,(skdata,connected_devices))
                        else:
                            str1 = "Impossible to start a new sampling session:\n"
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
