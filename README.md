![logo](https://github.com/domenico-suriano/SentinAir/blob/master/images/sentinairlogo.jpg)

Project designer and developer

Dr. Domenico Suriano , domenico.suriano@enea.it

# Description

SentinAir is a device designed for data acquisition from diverse types of instruments, sensors or devices. This system was at first developed for air pollutant monitoring activities, but it can also be used in other fields. Through this tool, you can acquire data from gas sensors or devices that you can plug into SentinAir system by USB, Ethernet, serial, or I2C ports. This system is useful especially in activities performed far from the laboratory facilities. The minimum requirement necessary to use the SentinAir device is a 220 Volt a.c. power source. The system can be controlled from the remote through internet wireless connections or through the Wi-Fi LAN set up by the SentinAir device as soon as it starts up. You can use SentinAir, for example, as a portable monitoring unit for air pollutant concentration detection; or, for evaluating device, instrument and sensor performances. By clicking on the pictures below you can see an explanatory video about the SentinAir use. You can find detailed information about how to set up and use SentinAir in the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-user-guide-2.0.pdf) released in the "guide" folder of this repository. The description of the SentinAir system and its use are also shown in four scientific articles: [A portable air quality monitoring unit and a modular, flexible tool for on-field evaluation and calibration of low-cost gas sensors](https://doi.org/10.1016/j.ohx.2021.e00198) published on HardwareX by Elsevier, [SentinAir system software: A flexible tool for data acquisition from heterogeneous sensors and devices](https://doi.org/10.1016/j.softx.2020.100589) published on "SoftwareX" by Elsevier, [Design and Development of a Flexible, Plug-and-Play, Cost-Effective Tool for on-Field Evaluation of Gas Sensors](https://doi.org/10.1155/2020/8812025) published on "Journal of Sensors" by Hindawi, and [Assessment of the Performance of a Low-Cost Air Quality Monitor in an Indoor Environment through Different Calibration Models](https://doi.org/10.3390/atmos13040567) published on "Atmosphere" by MDPI. I hope it will be useful to you.

# SentinAir software quick installation
This is a quick procedure to install the SentinAir software making the minimum steps. If you desire a higher level of customization, you can refer to the “SentinAir software installation” chapter of the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-user-guide-2.0.pdf) released in this repository. To install SentinAir, download the [last SentinAir SD card image file](https://drive.google.com/file/d/1KaBjFTMJjB79ryGpAMCCBvThq09m7BA6/view?usp=sharing) (file size of 720 Mb), unzip the file, then write it in a SD card having at least 2 GB of memory space (4GB recommended) by using, for example, Win32diskimage.exe program (for Windows operative systems). Finally, insert the SD card in the slot of the Raspberry PI board.

# Using SentinAir
After following the "quick installation" procedure, plug into one of the system ports your sensors/devices/instruments and give power to the device. Wait for a few of seconds, you will see the green light asynchronously blinking (this indicates that the system is starting up). After few seconds, the yellow light will start blinking fastly. This means that the system is performing the port scanning and the devices/sensor/instrument connection. Wait for few tens of seconds, then the red check light will turn on. When the yellow light stops blinking and turns on, the system is ready and it is already performing the data acquisition. To shut down SentinAir, press for few seconds the "stop button", then the yellow check light will start blinking. Wait for each light turns off, then unplug the power cable. For more detials to use the SentinAir system, please, refer to the [user guide](https://github.com/domenico-suriano/SentinAir/blob/master/guide/sentinair-user-guide-2.0.pdf) released in this repository. An overview of the SentinAir system use is shown in the video you can see by clicking on the pictures at the bottom of this page.
Here below are summarized the instruments which drivers have been already developed and incorporated in the sentinAIr software, and therefore, readily usable with sentinAir.
| Device | Device driver | Connection interface | Supplier or manufacturer |
|     :---:    |            :---:            |                      :---:                   |                         :---:                        |
|106L GO3 pro package (CO2and O3 monitor)|[go3.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/go3.py)|USB|[2B technologies](https://www.twobtech.com)|
|405nm (NOx monitor)|[nox405.py ](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/nox405.py)|USB|2B technologies|
|CO12M (CO chemical analyzer)|[co12m.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/co12m.py) |Ethernet port|[Environnement](https://www.envea.global)|
|AF22M (SO2 chemical analyzer)|[af22.py ](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/af22.py)|Ethernet port|Environnement|
|AC32M (NOx chemical analyzer)|[ac32.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/ac32.py) |Ethernet port|Environnement|
|O342M (O3 chemical analyzer)|[o342.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/o342.py) |Ethernet port|Environnement|
|VOC72M (VOCchemical analyzer)|[v72m.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/v72m.py) |Ethernet port|Environnement|

Here below are listed the sensors having a I2C, TTL serial port, or USB hardware interface, which drivers have been already developed and incorporated in the sentinAIr software, and therefore, readily usable with sentinAir. This list does not include the sensors featured by only an analog output interface.

| Sensor | Sensor driver | Connection interface | Supplier or manufacturer |
|     :---:    |            :---:            |                      :---:                   |                         :---:                        |
|BME280 (atmospheric pressure, temperature, and relative humidity)|[bme280.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/bme280.py)|I2C|[Bosch Sensortec](https://www.bosch-sensortec.com)|
|BH1750 (luxmeter)|[bh1750.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/bh1750.py) |I2C|[ROHM semiconductor](https://www.rohm.com)|
|PMS5003 (PM sensor)|[pms5003.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/pms5003.py) |TTL serial port|[Plantower](https://www.plantower.com/en/)|
|PMS3003 (PM sensor)|[pms3003.py ](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/pms3003.py)|TTL serial port|Plantower|
|MHZ19 (CO2 sensor)|[mhz19.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/mhz19.py) |TTL serial port|[Winsen](https://www.winsen-sensor.com)|
|IRC-A1 (CO2 sensor)|[irca1.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/irca1.py) |USB|[Alphasense](https://www.alphasense.com/product_type/target-gas/)|
|SPS30 (PM sensor)|[sps30.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/sps30.py) |TTL serial port|[Sensirion](https://sensirion.com)|

In order to use the sensors featured by just the analog hardware interface, drivers for some Analog-to-DIgital Converter (ADC) boards have been already developed and incorporated in the SentinAIr software. Currently, they are the [ADC Pi board](https://www.abelectronics.co.uk/p/69/adc-pi-raspberry-pi-analogue-to-digital-converter) (which driver is [mcp342x.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/mcp342x.py)) by [ABelectronics](https://www.abelectronics.co.uk/), the [Multisensor board](https://www.tecnosens.it/en/multisensor) (which driver is [multisensor_board.py](https://github.com/domenico-suriano/SentinAir/blob/master/sentinair/devices/multisensor_board.py)) by [Tecnosens](https://www.tecnosens.it/en), and the Lcss adapter which is an open source project you can find [here](https://github.com/domenico-suriano/Lcss-adapter-board).

In the list shown below, there are some examples of sensors featured by an analog output signal that can be readily used in the SentinAir system. The list does not cover every sensor or device available on the market usable with SentinAir, because its purpose is just to provide an idea about the flexibility of the system proposed. Therefore, this is a partial list which wants to provide some examples. Moreover, we must consider that any analog sensor has to be used through its support board, usually provided by the manufacturer, or the supplier, or built by the user, and one of the boards acting as adapter to the SentinAir system, such as: the ADC Pi board, the LCSS adapter, or the Multisensor board.

| Sensor | Support board name | Adapter board| Sensor supplier or manufacturer |
|     :---:    |            :---:            |                      :---:                   |                         :---:                        |
|CO-BX (CO sensor)|[ISB by Alphasense](https://www.alphasense.com/products/support-circuits-air/) or [Alphasense-B4-multisensor-board](https://github.com/domenico-suriano/Alphasense-B4-multisensor-board) |ADC Pi or LCSS adapter|[Alphasense](https://www.alphasense.com)|
|NO2-B43F (NO2 sensor)|ISB by Alphasense or Alphasense-B4-multisensor-board|ADC Pi or LCSS adapter|Alphasense|
|NO-B4 (NO sensor)|ISB by Alphasense |ADC Pi or LCSS adapter|Alphasense|
|OX-B431 (O3 sensor)|ISB by Alphasense or Alphasense-B4-multisensor-board|ADC Pi or LCSS adapter|Alphasense|
|SO2-B4 (SO2 sensor)|ISB by Alphasense or Alphasense-B4-multisensor-board|ADC Pi or LCSS adapter|Alphasense|
|H2S-B4 (H2S sensor)|ISB by Alphasense or Alphasense-B4-multisensor-board|ADC Pi or LCSS adapter|Alphasense|
|CO-A4 (CO sensor)|[AFE by Alphasense](https://www.alphasense.com/products/support-circuits-air/)|ADC Pi or LCSS adapter|Alphasense|
|NO-A4 (NO sensor)|AFE by Alphasense|ADC Pi or LCSS adapter|Alphasense|
|SO2-A4 (SO2 sensor)|AFE by Alphasense|ADC Pi or LCSS adapter|Alphasense|
|OX-A431 (O3 sensor)|AFE by Alphasense|ADC Pi or LCSS adapter|Alphasense|
|H2S-A4 (H2S sensor)|AFE by Alphasense|ADC Pi or LCSS adapter|Alphasense|
|PID-A12 (VOC sensor)|AFE by Alphasense|ADC Pi or LCSS adapter|Alphasense|
|PID-AH2 (VOC sensor)|AFE by Alphasense|ADC Pi or LCSS adapter|Alphasense|
|GS+4CO (CO sensor)|[AFE by TEcnosens](https://www.tecnosens.it/en/application-sectors/multigas-monitor/multisensor-board)|[Multisensor board by Tecnosens](https://www.tecnosens.it/en/application-sectors/multigas-monitor/multisensor-board)|[DDScientific](https://www.ddscientific.com)|
|GS+4ETO (ETO sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|DDScientific|
|GS+4NH3-100 (NH3 sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|DDScientific|
|GS+4NO (NO sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|DDScientific|
|GS+4NO2 (NO2 sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|DDScientific|
|GS+4CL2 (Cl2 sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|DDScientific|
|GS+4SO2 (SO2 sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|DDScientific|
|TDS 0035(CH4 sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|[Dynament](https://www.dynament.com/data-old/premier-series/)|
|TDS 0058(CO2 sensor)|AFE by TEcnosens|Multisensor board by Tecnosens|[Dynament](https://www.dynament.com/data-old/premier-series/)|
|SP61 (O3 sensor)|[A1320301-SP61-01 by Nissha](https://www.fisinc.co.jp/en/products/products_search.html?Cat=Cat2)|ADC Pi or LCSS adapter|[Nissha-Fis](https://www.fisinc.co.jp/en/)|
|SP61 (O3 sensor)|A1320301-SP61-02 by Nissha|ADC Pi|Nissha-Fis|
|SPS-AQ2-01 (VOC sensor)|EVM-SP-02-SP3S by Nissha|ADC Pi|Nissha-Fis|
|SB-xx (SB series sensor for various gases)|[EVM-SB-01-xx by Nissha](https://www.fisinc.co.jp/en/products/products_search.html?Cat=Cat2)|ADC Pi|Nissha-Fis|
|SP-xx (SP series sensor for various gases)|[EVM-SP-01-xx by Nissha](https://www.fisinc.co.jp/en/products/products_search.html?Cat=Cat2)|ADC Pi|Nissha-Fis|
|TGS26xx (TGS26 series sensor for various gases)|[EM26 by Figaro](https://www.figarosensor.com/product/evaluation-board/)|ADC Pi|[Figaro](https://www.figarosensor.com)|
|FECSxx (FECS series sensor for various gases)|[EM-FECS(B) by Figaro](https://www.figarosensor.com/product/evaluation-board/)|ADC Pi|Figaro|
|ME2-CO (CO sensor)|[ZE07-CO by Winsen](https://www.winsen-sensor.com/sensors/co-sensor/ze07-co.html)|ADC Pi or LCSS adapter|[Winsen](https://www.winsen-sensor.com/)|

# Last Updates

16 december 2023

-a) removed the lighttpd http server

-b) updated "sentinair-system-manager.py" to optimize the hourly and daily calulations, to incorporate the http server and to add the graphical user interface through the new web pages

-c) modified the structure of the sentinair software directories

-d) updated "sentinair-system-installer.py" to improve the "user-friendly" grade

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
