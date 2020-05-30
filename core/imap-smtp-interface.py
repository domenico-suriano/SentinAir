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

import smtplib
import time
import imaplib
import email
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys
import socket
import os
import signal
import logging
import _thread

## imap/smtp connection settings and e-mail account
FROM_EMAIL  = "" 
FROM_PWD    = "" 
SMTP_SERVER = "" 
IMAP_SERVER = ""

## path of the file in charge of monitoring the activity of this module
MONITOR_FILE = "/home/pi/sentinair/imap-smtp-monitor.sh"

## settings of the idp socket for the communications with sentinair system manager module
UDP_SERVICE_PORT = 16670
UDP_SERVER_ADDRESS = ('localhost', UDP_SERVICE_PORT)

## end string marker
END_STR = ">>>end__"

## path of the log file
LOGFILE = '/var/www/html/log/imap-smtp-interface-log.txt'

## module settings
GREETINGS_ATTEMPTS = 5
TIMEOUT_WATCHDOG = 300

## function in charge of reading emails from imap server,
## if a message for sentinair is found, the string containing
## the command is returned
def read_email_from_mail(cmd,sycs,sucs):
    comm = ""
    mail_ids = ""
    result = ""
    data = []
    idm = []
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        result, data = mail.search(None,'(FROM "domenico.suriano@enea.it" SUBJECT ' + "\"" + cmd + "\"" + ')')
        mail_ids1 = data[0]
        mail_ids = mail_ids1.decode()
    except Exception as e:
        logging.warning("ERROR occurred in searching mail : " + str(e))
    if mail_ids != "":
        idm = mail_ids.split(' ')
        ss = 0
        while ss < len(idm):
            try:
                typ, data = mail.fetch(idm[ss], '(RFC822)' )
                body1 = data[0][1]
                body = body1.decode()
                bodypieces = body.split("Subject: ")
                strsub = bodypieces[1]
                strsub1 = strsub.split("\r\n")
            except Exception as e1:
                logging.warning("ERROR occurred in fetching mail : " + str(e1))
            if (strsub1[0]==sycs) or (strsub1[0]==sucs):    
                try:
                    com1 = body.split("do: ")
                    com = com1[1].split("\r\n")
                    comm = com[0].lstrip()
                except Exception as e1:
                    logging.warning("ERROR occurred in parsing mail text : " + str(e1))
                try:
                    mail.store(idm[ss], '+FLAGS', '\\Deleted')
                    mail.expunge()
                except Exception as e2:
                    logging.warning("ERROR occurred in deleting mail : " + str(e2))
                    pass
            ss = ss + 1
    try:
        mail.close()
        mail.logout()
        return comm
    except:
        return comm


## function to start the watchdog for avoiding the module lock
def start_watchdog(pp1):
    global control
    control = 10
    try:
        _thread.start_new_thread(watchdog,(pp1,))
    except Exception as e:
        pass



def stop_watchdog():
    global control
    control = 0


## module watchdog, if the module got blocked, it got killed,
## then the imap-smtp-monitor.sh will provide to re-start it
def watchdog(pp):
    global control
    while (control > 9) and (control < TIMEOUT_WATCHDOG):
        time.sleep(1)
        control = control + 1
    if control >= TIMEOUT_WATCHDOG:
        logging.warning("CRITICAL ERROR in connecting mail server: program got blocked!")
        os.kill(pp, signal.SIGKILL)
        sys.exit(0)

## function in charge of sending emails through the smtp server
def send_mail(body,subj,fn1):
    try: 
        if fn1 != "":
            filename = fn1
            attachment = open(fn1, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            fn2 = filename.split('/')
            a = len(fn2)-1
            if a < 0:
                a = 0
            part.add_header('Content-Disposition', "attachment; filename= %s" % fn2[a])
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, 'plain'))
            msg.attach(part)
        else:
            msg = MIMEText(body)
        msg['From'] = FROM_EMAIL
        msg['To'] = FROM_EMAIL
        msg['Subject'] = subj
        server = smtplib.SMTP(SMTP_SERVER, 25)
        server.starttls()
        server.login(FROM_EMAIL, FROM_PWD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, FROM_EMAIL, text)
    except Exception as e1:
        logging.warning("ERROR occurred in sending mail : " + str(e1))
        return "sending FAILED"
    try:
        server.quit()
        return "sending OK"
    except Exception as e1:
        logging.warning("ERROR occurred in quitting mail server : " + str(e1))
        return "sending OK"

## function to execute commands for the operative system
def run_system_command(cmd):
    resp = ""
    try:
        resp1 = subprocess.check_output(cmd, shell = True)
        resp = resp1.decode()
    except Exception as e1:
        resp = str(e1)
    return resp

## function for getting files to send through e-mail in attach
def run_system_command_2(cmd):
    resp = None
    if cmd[0:4] == 'fget':
        cmd1 = cmd.split(' ')
        if len(cmd1)>0:
            if os.path.isfile(cmd1[1]):
                resp = "OK, file sent in attach\r\n"
                filen = cmd1[1]
                return resp,filen
            else:
                resp = "Sorry! " + cmd1[1] + "file not exist\r\n"
                filen = ""
                return resp,filen
        else:
            resp = "Error. You must type: get <file name with path>\r\n"
            filen = ""
            return resp,filen
    try:
        os.system(cmd + '> tmpdata 2>&1')
        resp1 = open('tmpdata','r').read()
        os.remove('tmpdata')
        filen = ""
        if resp1 == "":
            resp = resp1 + "OK, done\r\n"
        else:
            resp = resp1
    except Exception as e:
        resp = "ERROR occurred in executing system command: \r\n" + str(e1)
        logging.warning("ERROR occurred in executing system command: " + str(e1))
    return resp, filen


#######################            
######### MAIN ########
#######################
global control
global pid
### check if this module is configured, otherwise it exits
if (FROM_EMAIL=="") or (FROM_PWD=="") or (SMTP_SERVER =="") or (IMAP_SERVER==""):
    sys.exit(0)
time.sleep(5)
pid = os.getpid()
control = 0
## retrieving device name
try:
    f = open("/etc/hostname","r")
    machine_name = f.readline().rstrip("\r\n")
    f.close()
    pn = machine_name.split("-")
    machine_nick = pn[1]
except:
    machine_name = "Sentinair-SX"
    machine_nick = "SX"
## preparing strings to insert in e-mail messages
system_cmd = machine_nick + ' system command'
surianocli_cmd = machine_nick + ' SentinAir command'
system_cmd_str = machine_nick + ' system command'
surianocli_cmd_str = machine_nick + ' SentinAir command'
subj_resp_sys = machine_name + " system response"
subj_resp_cli = machine_name + " SentinAir response"
subj_resp_str = machine_name + " just started"
## initalizing the log file
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG,format='%(asctime)s - %(message)s',datefmt='%d/%m/%Y_%H:%M:%S')
if len(sys.argv)==1:
    print ("\n" + machine_name + " imap-smtp interface started...\n")
    logging.info(machine_name  + ' imap-smtp interface started...')
res = ""
## setting up udp socket for communication with sentinair system manager
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(200)
except:
    res = "Impossible to communicate with SentinAir! Try reboot!"
    logging.warning('Impossible to communicate with SentinAir! Try reboot')

#### starting imap-smtp interface monitor
try:
    os.system("sh " + MONITOR_FILE + "&")
except Exception as e:
    logging.warning("Imap-smtp monitor starting failed:",exc_info=True)
## at sentinair start up an e-mail is sent with sentinair status information,
## cpu temperature, and date/time of the system
if len(sys.argv)==1:
    if res == "":
        try:
            data3 = ""
            data1 = ""
            sent = sock.sendto('i'.encode(), UDP_SERVER_ADDRESS)
            ss = 0
            while ((data3.find(END_STR) == -1) and (ss < 5)):
                try:
                    data, server = sock.recvfrom(2048)
                    data3 = data.decode()
                    data1 = data3.rstrip(END_STR)
                except Exception as e:
                    ss = ss + 1
                    logging.warning("Connection with SentinAir error: " + str(e))
                    data = "No connection SentinAir manager!\r\n"
                    data2 = data
            data2 = str(data1)
        except socket.timeout:
            data2 = "\r\nSentinAir is not responding. Try rebooting!\r\n"    
    else:
        data2 = res
    try:
        tt = "Date/time on " + machine_name + " now is " + time.strftime("%d/%m/%Y %H:%M:%S") + ".\r\n"
    except:
        tt = machine_name + " date/time unavailable.\r\n"
    try:
        temp1 = os.popen("vcgencmd measure_temp").readline()
        temp2 = temp1.rstrip("'C\r\n\r\n")
        temp3 = temp2.replace("temp=","")
        tt = tt + "Cpu temperature on " + machine_name + " now is " + temp3 + " C.\r\n"
    except:
        tt = tt + "Cpu temperature on " + machine_name + " unavailable.\r\n"
    helpstr = "\nTo send commands for SentinAir system, send email with \"Sx SentinAir command\" as subject, "+\
              "where x is the SentinAir device number (for example S1).\n"+\
              "In the body mail write \"do: [command]\", where [command] could be:\n"+\
              "h for help,\ni for getting info on SentinAir status,\nb for breaking the current monitoring,\n"+\
              "c for checking on the devices connected to SentinAir,\ns for scanning the devices plugged to SentinAir,\n"+\
              "s,[seconds] for starting a new monitoring session at [seconds] rate\n"
    greet = 0
    while (greet<GREETINGS_ATTEMPTS):
        start_watchdog(pid)
        res = send_mail(machine_name + " ready!\r\n" + tt + helpstr + "\r\n" + data2 + "\r\n",subj_resp_str,"")
        stop_watchdog()
        logging.info(machine_name + " ready!\r\n" + tt + helpstr + "\r\n" + data2 + "\r\n")
        if res == "sending OK":
            break
        greet = greet + 1
        time.sleep(20)
## if the inital e-mail sending fails, the module got restarted
    if (greet>=GREETINGS_ATTEMPTS):
        os.kill(pid, signal.SIGKILL)
else:
    logging.info(machine_name + " restarted...")    

## infinite loop to get command messages from emails and send system responses
while 1:
    time.sleep(15)
    start_watchdog(pid)
    cmd = read_email_from_mail(system_cmd,system_cmd_str,surianocli_cmd_str)
    stop_watchdog()
    if cmd != "":### a valid command is arrived
        rr,fn = run_system_command_2(cmd)
        cmd1 = cmd.rstrip()
        cmd2 = cmd1.rstrip("\r\n")
        if cmd2 != "reboot":
            time.sleep(5)
            try:
                tt = "Date/time on " + machine_name + " now is " + time.strftime("%d/%m/%Y %H:%M:%S") + ".\r\n"
            except:
                tt = machine_name + " date/time unavailable.\r\n"
            try:
                temp1 = os.popen("vcgencmd measure_temp").readline()
                temp2 = temp1.rstrip("'C\r\n\r\n")
                temp3 = temp2.replace("temp=","")
                tt = tt + "Cpu temperature on " + machine_name + " now is " + temp3 + " C.\r\n"
            except:
                tt = tt + "Cpu temperature on " + machine_name + " unavailable.\r\n"
            greet = 0
            while (greet<GREETINGS_ATTEMPTS):
                start_watchdog(pid)
                res = send_mail(tt + "Response for system command " + chr(34) + cmd + chr(34) + ":\r\n" +  rr,subj_resp_sys,fn)
                stop_watchdog()
                if res == "sending OK":
                    break
                greet = greet + 1
                time.sleep(10) 
    time.sleep(15)
    start_watchdog(pid)
    cmdcli1 = read_email_from_mail(surianocli_cmd,system_cmd_str,surianocli_cmd_str)
    stop_watchdog()
    file_n = ""
    if cmdcli1 != "":
        cmdcli2 = cmdcli1.rstrip()
        cmdcli = cmdcli2.rstrip("\r\n")
        try:
            data2 = ""
            buf = []
            sent = sock.sendto(cmdcli.encode(), UDP_SERVER_ADDRESS)
            while (data2.find(END_STR) == -1):
                try:
                    data, server = sock.recvfrom(2048)
                    data2 = data.decode()
                except Exception as e:
                    data1 = "\r\nSentinAir is not responding. Try again or reboot!\r\n"
                    logging.warning('SentinAir is not responding. Try again or reboot')
                    break
                buf.append(str(data2) + "\r\n")
                buf1 = ''.join(buf)
                data1 = buf1.rstrip(END_STR + "\r\n")
        except socket.timeout:
            data1 = "\r\nSentinAir is taking too much to answer. Try again or reboot!\r\n"
            logging.warning('SentinAir is taking too much to answer. Try again or reboot!')
        time.sleep(15)
        try:
            tt = "Date/time on " + machine_name + " now is " + time.strftime("%d/%m/%Y %H:%M:%S") + ".\r\n"
        except:
            tt =  machine_name + " date/time unavailable.\r\n"
        try:
            temp1 = os.popen("vcgencmd measure_temp").readline()
            temp2 = temp1.rstrip("'C\r\n\r\n")
            temp3 = temp2.replace("temp=","")
            tt = tt + "Cpu temperature on " + machine_name + " now is " + temp3 + " C.\r\n"
        except:
            tt = tt + "Cpu temperature on " + machine_name + " unavailable.\r\n"
        greet = 0
        while (greet<GREETINGS_ATTEMPTS):
            start_watchdog(pid)
            res = send_mail(tt + "Response for SentinAir command "  + chr(34) + cmdcli + chr(34) + ":\r\n" +  data1, subj_resp_cli,file_n)
            stop_watchdog()
            if res == "sending OK":
                break
            greet = greet + 1
            time.sleep(10)
