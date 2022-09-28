![logo](https://github.com/domenico-suriano/SentinAir/blob/master/images/sentinairlogo.jpg)

Project designer and developer

Dr. Domenico Suriano , domenico.suriano@enea.it

# Description

SentinAir is a device designed for data acquisition from diverse types of instruments, sensors or devices. This system was at first developed for air pollutant monitoring activities, but it can also be used in other fields. Through this tool, you can acquire data from gas sensors or devices that you can plug into SentinAir system by USB, Ethernet, serial, or I2C ports. This system is useful especially in activities performed far from the laboratory facilities. The minimum requirement necessary to use the SentinAir device is a 220 Volt a.c. power source. The system can be controlled from the remote through internet wireless connections or through the Wi-Fi LAN set up by the SentinAir device as soon as it starts up. You can use SentinAir, for example, as a portable monitoring unit for air pollutant concentration detection; or, for evaluating device, instrument and sensor performances. By clicking on the pictures below you can see an explanatory video about the SentinAir use. You can find detailed information about how to set up and use SentinAir in the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-user-guide-1.41.pdf) released in the "guide" folder of this repository. The description of the SentinAir system and its use are also shown in four scientific articles: [A portable air quality monitoring unit and a modular, flexible tool for on-field evaluation and calibration of low-cost gas sensors](https://doi.org/10.1016/j.ohx.2021.e00198) published on HardwareX by Elsevier, [SentinAir system software: A flexible tool for data acquisition from heterogeneous sensors and devices](https://doi.org/10.1016/j.softx.2020.100589) published on "SoftwareX" by Elsevier, [Design and Development of a Flexible, Plug-and-Play, Cost-Effective Tool for on-Field Evaluation of Gas Sensors](https://doi.org/10.1155/2020/8812025) published on "Journal of Sensors" by Hindawi, and [Assessment of the Performance of a Low-Cost Air Quality Monitor in an Indoor Environment through Different Calibration Models](https://doi.org/10.3390/atmos13040567) published on "Atmosphere" by MDPI. I hope it will be useful to you.

# SentinAir software quick installation
This is a quick procedure to install the SentinAir software making the minimum steps. If you desire a higher level of customization, you can refer to the “SentinAir software installation” chapter of the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-user-guide-1.41.pdf) released in this repository. To install SentinAir, download the [last SentinAir SD card image file](https://drive.google.com/file/d/1HvyRzrcsKjluTnoz6XaY3P8Az7UpIHC8/view?usp=sharing) (file size of 610 Mb), unzip the file, then write it in a SD card having at least 2 GB of memory space (4GB recommended) by using, for example, Win32diskimage.exe program (for Windows operative systems). Finally, insert the SD card in the slot of the Raspberry PI board.

# Using SentinAir
After following the "quick installation" procedure, plug into one of the system ports your sensors/devices/instruments and give power to the device. Wait for a few of seconds, you will see the green light asynchronously blinking (this indicates that the system is starting up). After few seconds, the yellow light will start blinking fastly. This means that the system is performing the port scanning and the devices/sensor/instrument connection. Wait for few tens of seconds, then the red check light will turn on. When the yellow light stops blinking and turns on, the system is ready and it is already performing the data acquisition. To shut down SentinAir, press for few seconds the "stop button", then the yellow check light will start blinking. Wait for each light turns off, then unplug the power cable. For more detials to use the SentinAir system, please, refer to the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-user-guide-1.41.pdf) released in this repository. An overview of the SentinAir system use is shown in the video you can see by clicking on the pictures at the bottom of this page.
Here below are summarized the instruments which drivers have been already developed and incorporated in the sentinAIr software, and therefore, readily usable with sentinAir.
| Device | Device driver | Connection interface | Supplier or manufacturer |
|     :---:    |            :---:            |                      :---:                   |                         :---:                        |
|106L GO3 pro package (CO2and O3 monitor)|[go3.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/go3.py)|USB|[2B technologies](https://www.twobtech.com)|
|405nm (NOx monitor)|[nox405.py ](https://github.com/domenico-suriano/SentinAir/blob/master/devices/nox405.py)|USB|2B technologies|
|CO12M (CO chemical analyzer)|[co12m.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/co12m.py) |Ethernet port|[Environnement](https://www.envea.global)|
|AF22M (SO2 chemical analyzer)|[af22.py ](https://github.com/domenico-suriano/SentinAir/blob/master/devices/af22.py)|Ethernet port|Environnement|
|AC32M (NOx chemical analyzer)|[ac32.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/ac32.py) |Ethernet port|Environnement|
|O342M (O3 chemical analyzer)|[o342.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/o342.py) |Ethernet port|Environnement|
|VOC72M (VOCchemical analyzer)|[v72m.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/v72m.py) |Ethernet port|Environnement|

Here below are listed the sensors having a I2C, TTL serial port, or USB hardware interface, which drivers have been already developed and incorporated in the sentinAIr software, and therefore, readily usable with sentinAir. This list does not include the sensors featured by only an analog output interface.

| Sensor | Sensor driver | Connection interface | Supplier or manufacturer |
|     :---:    |            :---:            |                      :---:                   |                         :---:                        |
|BME280 (atmospheric pressure, temperature, and relative humidity)|[bme280.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/bme280.py)|I2C|[Bosch Sensortec](https://www.bosch-sensortec.com)|
|BH1750 (luxmeter)|[bh1750.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/bh1750.py) |I2C|[ROHM semiconductor](https://www.rohm.com)|
|PMS5003 (PM sensor)|[pms5003.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/pms5003.py) |TTL serial port|[Plantower](https://www.plantower.com/en/)|
|PMS3003 (PM sensor)|[pms3003.py ](https://github.com/domenico-suriano/SentinAir/blob/master/devices/pms3003.py)|TTL serial port|Plantower|
|MHZ19 (CO2 sensor)|[mhz19.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/mhz19.py) |TTL serial port|[Winsen](https://www.winsen-sensor.com)|
|IRC-A1 (CO2 sensor)|[irca1.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/irca1.py) |USB|[Alphasense](https://www.alphasense.com/product_type/target-gas/)|
|SPS30 (PM sensor)|[sps30.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/sps30.py) |TTL serial port|[Sensirion](https://sensirion.com)|

In order to use the sensors featured by just the analog hardware interface, drivers for some Analog-to-DIgital Converter (ADC) boards have been already developed and incorporated in the SentinAIr software. Currently, they are the [ADC Pi board](https://www.abelectronics.co.uk/p/69/adc-pi-raspberry-pi-analogue-to-digital-converter) (which driver is [mcp342x.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/mcp342x.py)) by [ABelectronics](https://www.abelectronics.co.uk/), the [Multisensor board](https://www.tecnosens.it/en/multisensor) (which driver is [multisensor_board.py](https://github.com/domenico-suriano/SentinAir/blob/master/devices/multisensor_board.py)) by [Tecnosens](https://www.tecnosens.it/en), and the Lcss adapter which is an open source project you can find [here](https://github.com/domenico-suriano/Lcss-adapter-board) .

# Last Updates

26 september 2022

-a) updated "sentinair-system-manager.py" to fix a bug in logging the device scanning reports

-b) added the drivers for SPS30 (PM sensor), PMS5003 (PM sensor), and MHZ19 (CO2 sensor)

2 february 2021

-a) updated "sentinair-system-manager.py" to modify the check light behaviour

-b) added the driver for bme280 (temperature, humidity, and atmospheric pressure sensor)

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
