![logo](https://github.com/domenico-suriano/SentinAir/blob/master/images/sentinairlogo.jpg)

Project designer and developer

Dr. Domenico Suriano , domenico.suriano@enea.it

# Description

SentinAir is a device designed and developed for data acquisition from diverse types of instruments, sensors or devices. Through this tool, you can acquire data from devices that you can plug into SentinAir system by USB, Ethernet, serial, SPI, or I2C ports. This system is useful especially in activities performed far from the laboratory facilities. The minimum requirement necessary to use the SentinAir device is a 220 Volt a.c. power source. The system can be controlled from the remote through internet wireless connections or through the Wi-Fi LAN set up by the SentinAir device as soon as it starts up. You can use SentinAir, for example, as a portable monitoring unit for air pollutant concentration detection; or, for evaluating device, instrument and sensor performances. By clicking on the pictures below you can see an explanatory video about the SentinAir use. You can find detailed information about how to set up and use SentinAir in the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-system-user-guide.pdf) released in the "guide" folder of this repository. The description of the SentinAir system and its use are shown in two scientific articles: [SentinAir system software: A flexible tool for data acquisition from heterogeneous sensors and devices](https://doi.org/10.1016/j.softx.2020.100589) published on "SoftwareX" by Elsevier, and [Design and Development of a Flexible, Plug-and-Play, Cost-Effective Tool for on-Field Evaluation of Gas Sensors](https://doi.org/10.1155/2020/8812025) published on "Journal of Sensors" by Hindawi.
I hope it will be useful to you.

# SentinAir software quick installation
This is a quick procedure to install the SentinAir software making the minimum steps. If you desire a higher level of customization, you can refer to the “SentinAir software installation” chapter of the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-system-user-guide.pdf) released in this repository. To install SentinAir, download the [last SentinAir SD card image file](https://drive.google.com/file/d/1Ex4GyDE1UydjNPgzCsWaSeaUH6ddkkUb/view?usp=sharing) (file size of 550 Mb), unzip the file, then write it in a SD card having at least 2 GB of memory space (4GB recommended) by using, for example, Win32diskimage.exe program (for Windows operative systems). Finally, insert the SD card in the slot of the Raspberry PI board.

# Using SentinAir
After following the "quick installation" procedure, plug into one of the system ports your sensors/devices/instruments and give power to the device. Wait for a few of seconds, you will see the red light blinking. This means that the system is performing the port scanning and the devices/sensor/instrument connection. Wait for few tens of seconds, then the red check light will stop blinking and, if any sensor/device/instrument is plugged into SentinAir, the green light will turn on. The system is ready and it is already performing the data acquisition. To shut down SentinAir, press for few seconds the "stop button", then the red check light will start blinking. Wait for the red light turning off, then after further 5 or 6 seconds, turn off the power. For more detials to use the SentinAir system, please, refer to the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-system-user-guide.pdf) released in this repository. An overview of the SentinAir system use is shown in the video you can see by clicking on the pictures below.

# Last Updates

11 november 2020:

-a) updated "sentinair-system-manager.py" to support I2C devices

-b) added drivers for bh1750 (luxmeter) and mcp342x (ADC Pi converter)

-c) updated the user guide. More clarifications and examples concerning "How to write new device drivers". Added information about the use of the ADC Pi.

-d) added device driver templates to facilitate the process of writing new device drivers (see the user guide).

-e) published the release of the version 1.2

-f) [SentinAir SD card image file](https://drive.google.com/file/d/1Ex4GyDE1UydjNPgzCsWaSeaUH6ddkkUb/view?usp=sharing) updated.

7 october 2020:

-a) minor bugs fixed.

-b) the red check light now blinks during the port scanning at start-up time.

-c) configuration of the module "imap-smtp-interface.py" by editing the file "mail-config.sentinair" (please refer to the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-system-user-guide.pdf) for details),

-d) User guide updated,

-e) release [sentinair_1.0.zip](https://github.com/domenico-suriano/SentinAir/releases/download/1.0/sentinair-1.0.zip) updated,

-f) [SentinAir SD card image file](https://drive.google.com/file/d/1AfPUjvr3tC3ymnK-TsBThjoi5kFb1ZuD/view?usp=sharing) updated.

30 september 2020:

-a) user guide updated,

-b) some minor bugs fixed.

[![sentinair](https://github.com/domenico-suriano/SentinAir/blob/master/images/sentinairdevice.jpg)](https://youtu.be/oAHfk2gzcIE)
[![how to use SentinAir](https://github.com/domenico-suriano/SentinAir/blob/master/video/video-still-1.jpg)](https://youtu.be/oAHfk2gzcIE)
