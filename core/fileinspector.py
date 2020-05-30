#!/usr/bin/python

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

import cgi

# path where files containing data are placed
DATAPATH = "/var/www/html/data/"
## path where files containing data plots are placed
IMGPATH = "/img/"

## function to get plots images to insert in the web page
def get_plots(filename):
    csvfile = open(filename,'r')
    hd1 = csvfile.readline()
    csvfile.close()
    hd = hd1.rstrip("\r\n")
    header = hd.split(";")
    return header   

## function to build the web page in the correct format
def print_page_meas(filename,head,mcn):
    fn = filename.rstrip("txt")
    print ("Content-type: text/html\n")
    print ('<html><head>')
    print ('<title>' + "Measure page in file " + fn + " on " + mcn + '</title>')
    print ('<style type=\"text/css\"> body { background-image: url(\"/sentinair.jpg\");background-size: cover;}</style>') 
    print ('</head><body>')
    print ('<p><h2><font face = \"arial\"> Here below are plots from<br>' + fn.rstrip(".") + '<br>on<br>' + mcn + '</font></h2></p>')
    print ('<table>')
    hnum = 0
    for h in head:
        if hnum == 0:
            hnum=hnum+1
        else:
            print ('<tr><td>')
            h=h.replace('%','')
            h=h.replace('/','')
            print ('<img alt=\"Data plot unavailable\" src=\"' + IMGPATH + fn + h + '.png\">')
            print ('</td></tr>')
            hnum=hnum+1
    print ('</table>')
    print ('</body></html>')
    
##### MAIN #########
fs = cgi.FieldStorage()
fn = DATAPATH + str(fs["fn"].value)
mn = str(fs["mn"].value)
hd = get_plots(fn)
print_page_meas(str(fs["fn"].value),hd,mn)

