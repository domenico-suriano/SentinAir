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

from lcss_adapter import Lcss_adapter
import serial.tools.list_ports
import _thread
import time
import sys

MAX_SAMPLING_RATE = 3


def search(conn_dev):
   conn_dev.clear()
   print("Searching for Lcss adapter boards...")
   ports = list(serial.tools.list_ports.comports())
   for prt in ports:
      lc = Lcss_adapter()
      res = lc.connect(prt[0])
      print("Scanning on port \"" + str(prt[0]) + "\"...")
      if res == 1:
          conn_dev.append(lc)
          print("Found " + conn_dev[-1].getIdentity())
   if len(conn_dev) == 0:
      print("No Lcss adapter found!")
   return conn_dev


def print_on_consolle(idb,m,v):
   mm = m.replace(";","   ")
   vv = v.replace(";","  ")
   print("")
   print(idb)
   print(mm)
   print(vv)
   sys.stdout.write(">> ")
   sys.stdout.flush()


def capture(conn_dev):
   global rate
   fh = init_session(conn_dev)
   while (rate != 0):
      vals = time.strftime("%Y-%m-%d_%H-%M-%S") + ";"
      for cn in conn_dev:
         idboard = cn.getIdentity()
         meas = cn.getSensors()
         curr_vals = cn.sample()
         vals = vals + curr_vals + ";"
         print_on_consolle(idboard,meas,curr_vals)
      make_record(vals.rstrip(";"),fh)
      time.sleep(rate)
   close_session(fh)


def show_help():
   print("LCSS ADAPTER CONSOLLE v1.0")
   print("Available commands are:")
   print("s (to search for lcss adapter board connected)")
   print("s,[seconds] (to start measurements at [seconds] sampling rate)")
   print("b (to stop measurements)")
   print("q (to quit the program)")


def init_session(conn_dev):
   try:
      filename = time.strftime("%Y-%m-%d_%H-%M-%S") + ".dat"
      f_handle = open(filename,  'w')
   except Exception as e:
      print(str(e))                  
      print("WARNING! Measurement will not be stored")
      return None
   f_handle = open(filename,  'w')
   head = "Date/time;"
   for cn in conn_dev:
      sens = cn.getSensors()
      sensl = sens.split(";")
      ids = cn.getIdentity()
      for s in sensl:
         head = head + ids + "_" + s + ";"
   head1 = head.rstrip(";")
   f_handle.write(head1 + "\n")
   f_handle.flush()
   return f_handle


def close_session(f):
   try:
      f.close()
   except Exception as e:
      pass


def make_record(rec,f):
   try:
      rec1 = rec.replace(".",",")
      f.write(rec1 + "\n")
      f.flush()
   except Exception as e:
      pass
   


global rate
rate = 0
connected_devices = []
show_help()
connected_devices = search(connected_devices)
while 1:
   comm = input(">> ")
   if comm == "h":
         show_help()
   if comm == 'q':
      sys.exit(0)
   if comm == "s":
      if rate > 0:
         print("Impossible executing command: first stop the measurements")
         continue
      connected_devices = search(connected_devices)
   if comm == 'b':
      rate = 0
      print("Measurements stopped")
   if (comm.find('s') == 0) and(len(comm)>1):
      if rate > 0:
         print("Measurements already running!")
         continue
      if len(connected_devices) == 0:
         print("No Lcss adapter connected. Measurements won't start")
         continue
      par = comm.split(',')
      try:
         rt = int(par[1])
         if rt < MAX_SAMPLING_RATE:
            print("Sampling rate must be greater or equal " +  str(MAX_SAMPLING_RATE) +  " sec!")
            continue
         rate = rt
         _thread.start_new_thread(capture,(connected_devices,))
      except Exception as e:
          print("Command not valid: type s,[integer number]")
