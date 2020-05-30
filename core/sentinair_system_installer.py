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

## name of the sentinair system manger
MANAGER_FILE = "sentinair_system_manager.py"
### default path where sentinair system is located
DEFAULT_DIR = "/home/pi/sentinair"

import os
import sys
import time

def welcome_message():
    print ("\nSENTINAIR SYSTEM DEVICES DRIVERS INSTALLER 1.0")
    print ("This sotware has been witten by Dr. Domenico Suriano for SentinAir system.")

### function to display device drivers installer commands
def show_commands():
    print ("\nThese are the commands available in SentinAir system installer:")
    print ("1) to modify the path where \"sentinair_system_manager.py\" is located,")
    print ("press \'m\' and the \"Enter\" key")
    print ("2) to check what devices are installed, press \'c\' and then the \"Enter\" key")
    print ("3) to uninstall devices, type \"u,your_device_file_name.py\" and then the \"Enter\" key")
    print ("4) to install devices, type \"i,your_device_file_name.py\" and then the \"Enter\" key")
    print ("5) to get help, press \'h\' and the \"Enter\" key")
    print ("6) to quit, press \'q\' and the \"Enter\" key\n")

## function to get the system manger path and storing it in the on purpose file
def modify_manager_path(mp):
    print ("Please, insert the complete path where \"sentinair_system_manager.py\" is located.")
    print ("For example type: /home/pi/sentinair")
    dirstr = input(">> ")
    if dirstr == 'q':
        sys.exit(0)
    mp = dirstr
    mp1 = mp.rstrip("/")
    mfile = mp1 + "/" + MANAGER_FILE
    print(mfile)
    if os.path.exists(mfile)==False:
        print ("Impossible to set SentinAir manager file path:")
        print ("SentinAir manager file does not exist in the directory.")
        return ""
    try:
        f1 = open(mp1 + "/" + "manager_dir.sentinair","w")
        f1.write(mp1)
        f1.close()
        print ("SentinAir manager file path set in: " + mp1)
        return mp1
    except Exception as e:
        return mp1  

### function to check what device drivers are currently installed in the system manager
def check_installed_device(mp):
    mp1 = mp + "/" + MANAGER_FILE
    try:
        f = open(mp1,"r")
        contents = f.readlines()
        found = False
        for line in contents:
            if line.find("installed_devices.append(") >= 0:
                strd = line.split("installed_devices.append(")
                dev1 = strd[1].split('_obj')
                print (dev1[0] + " is installed in SentinAir")
                found = True
        if found == False:
            print ("No device installed in SentinAir!")
    except Exception as e:
        print ("Impossible to read SentinAir system manager file!")

### function to uninstall device drivers in the system manager
def uninstall_device(named,mp):
    named = named.replace('\r','')
    named = named.replace('\n','')
    named1 = named.rstrip(".py")
    named2 = named1.capitalize()
    strtofind1 = "#" + named1 + " has been installed in SentinAir on "
    strtofind2 = "# do not remove or modify the next three lines below!!!\n"
    strtofind3 = "from devices." + named1 + " import " + named2
    strtofind4 = named1 + "_obj = " + named2 + "()"
    strtofind5 = "installed_devices.append(" + named1 + "_obj)"
    mp1 = mp + "/" + MANAGER_FILE
    try:
        f = open(mp1,"r")
        contents = f.readlines()
    except Exception as e:
        print ("Impossible to read " + mp1 + " file!")
        return
    found = False
    for line in contents:
        if line.find(strtofind1) == 0:
            contents.remove(line)
            break
    for line in contents:
        if line.find(strtofind2) == 0:
            contents.remove(line)
            break 
    for line in contents:
        if line.find(strtofind3) == 0:
            found = True
            contents.remove(line)
            break
    for line in contents:
        if line.find(strtofind4) == 0:
            found = True
            contents.remove(line)
            break
    for line in contents:
        if line.find(strtofind5) == 0:
            found = True
            contents.remove(line)
            break
    if found == False:
        print (named1 + " is not installed in SentinAir system.")
        return
    try:
        f = open(mp1,"w")
        contents = "".join(contents)
        f.write(contents)
        f.close()
        print (named1 + " successfully uninstalled from SentinAir system.")
    except Exception as e:
        print ("Impossible to write in " + mp1 + " file!")  
    
### function to install new device drivers in the system manager
def install_device(named,mp):
    named = named.replace('\r','')
    named = named.replace('\n','')
    named1 = named.rstrip(".py")
    named2 = named1.capitalize()
    strtofind1 = "installed_devices = []"
    dpath = mp + "/devices/" + named
    if os.path.exists(dpath)==False:
        print ("Impossible to install " + named + ":")
        print (named + " does not exist in " + mp + "/devices")
        return
    try:
        mp1 = mp + "/" + MANAGER_FILE
        f = open(mp1,"r")
        contents = f.readlines()
    except Exception as e:
        print ("Impossible to read " + mp1 + " file!")
        return
    for line in contents:
        if line.find("installed_devices.append(" + named1 + "_obj)") >= 0:
            print (named1 + " is already installed in SentinAir!")
            return
    nl = 0
    try:
        for line in contents:
            if line.find(strtofind1) == 0:
                toadd1 = "#" + named1 + " has been installed in SentinAir on " + time.strftime("%Y-%m-%d_%H-%M-%S") + "\n"
                toadd2 = "# do not remove or modify the next three lines below!!!\n"
                toadd3 = "from devices." + named1 + " import " + named2 + "\n"
                toadd4 = named1 + "_obj = " + named2 + "()\n"
                toadd5 = "installed_devices.append(" + named1 + "_obj)\n"
                contents.insert(nl + 1,toadd1)
                contents.insert(nl + 2,toadd2)
                contents.insert(nl + 3,toadd3)
                contents.insert(nl + 4,toadd4)
                contents.insert(nl + 5,toadd5)
            else:
                nl = nl + 1
    except Exception as e:
        pass
    try:
        f = open(mp1,"w")
        contents = "".join(contents)
        f.write(contents)
        f.close()
        print (named1 + " successfully installed in SentinAir!")
        print ("Remember to reboot the system later.")
    except Exception as e:
        print ("Impossible to write in " + mp1 + " file!")

    
def get_command():
    return input(">> ")
    


welcome_message()
show_commands()

try:
    f = open(DEFAULT_DIR + "/" + "manager_dir.sentinair","r")
    dirmanager = f.readline()
    mpath = dirmanager + "/" + MANAGER_FILE
    if os.path.exists(mpath)==False:
        dirmanager = ""
except Exception as e:
    dirmanager = ""

## if the file where is stored the path of the system manager is not found,
## then here the user has mandatory to insert it
while dirmanager == "":
   dirmanager = modify_manager_path(dirmanager)

## infinite loop to get user commands
while 1:
    cmd = get_command()
    if cmd == 'q':
        sys.exit(0)
    if cmd == 'h':
        show_commands()
        continue
    if cmd == 'm':## modify sentinair system path command arrived
        dirtemp = modify_manager_path(dirmanager)
        if dirtemp != "":
            dirmanager = dirmanager.replace(dirmanager,dirtemp)
        continue
    if cmd == 'c':##check installed devices command arrived
        check_installed_device(dirmanager)
        continue
    try:
        if (cmd[0] == 'u') and (cmd[1] == ','): ## uninstall driver command arrived
            cmd1 = cmd.split(',')
            uninstall_device(cmd1[1],dirmanager)
            continue
    except Exception as e:
        print ("Wrong command! Please retry.")
        continue
    try:
        if (cmd[0] == 'i') and (cmd[1] == ','):## install driver command arrived
            cmd1 = cmd.split(',')
            install_device(cmd1[1],dirmanager)
            continue
    except Exception as e:
        print ("Wrong command! Please retry.")
        continue    
    print ("Wrong command! Please retry.")
