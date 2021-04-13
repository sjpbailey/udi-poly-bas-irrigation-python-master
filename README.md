# BAS Irrigation NodeServer Using Contemporary Controls BASpi and the BASpi-Edge-6U6R BACnet Device Controller BACnet Wi-Fi IP

## Based on the Contemporary Controls BASpi and the BASpi-Edge SYS6U6R BACnet/IP Wi-Fi/IP Control Devices

* This controllers can be used to control low voltage switchable devices for any advanced control sequence attached via ethernet or Wi-Fi IP.

## Reasons

* The purpose of this Nodeserver is for custom control through the ISY for Irrigation and general Home automation for multiple control operations, WiFi, IP, BACnet.

* It utilizes up to six of the Contemporary Controls BASpi-6U6R and the BASpi-Edge-6U6R BACnet control Modules for up to thirty six (36) irrigation zones.
Please see links below for information & configuration of this Device within Contemporary Controls GUI.

* Each BASpi Controller with its six zone outputs also has six universal inputs with the first input configured for outside air temperature in degrees fahrenheit and the last input configured for moisture or volumetric water content sensor in percent using a 0-10vdc volumetric transmitter. Finally with inputs 2-4 for raw value UOM's for your choice in configuration.
So that's a total of thirty six zones and thirty six inputs, 12 reserved and 24 user configurable using up to six BASpi-6U6R and or the BASpi-Edge-6U6R controllers.

* It is Best to use the Open Weather Map Nodeserver to bring in your local weather conditions into your ISY to lock out your irrigation, if humidity, temperature, or even wind conditions make it unnessessary to water your landscaping! <https://github.com/bpaauwe/udi-owm-poly>

* This Network BAS series will include in the near future custom home control for Garage Door, Pool Control, Well Pump Control, HVAC, VVT, Boiler, along with any custom control you create utilizing the pip bascontrolns module <https://pypi.org/project/bascontrolns/>.

* This controller sits on a Raspberry Pi. You can easily add it to your ISY after you configure its ipaddress.

* Irrigation Polyglot Configuration

![BAS Irrigation Polyglot Configuration](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/4b0be27809dcd65ce32fec99b183681b35c28c68/Images/configuration-pagePM.png)

* Irrigation Controller

![BAS Irrigation Network Poly](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/4b0be27809dcd65ce32fec99b183681b35c28c68/Images/Controller.png)

* Irrigation Zone Node One

![Zone Control 1](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/dba72d56cee37816fd2656b4a0f3e39b34377395/Images/Zone-1-control.png)

* Irrigation Zone Node Two - These are repetitive for up to 6 Zone Nodes totaling 36 Zones. So 6, 12, 18, 24, 30, or 36 Zones depending on how many WiFi BASpi or BASpi-Edge Devices you have.

![Zone Control 2](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/dba72d56cee37816fd2656b4a0f3e39b34377395/Images/Zone-2-control.png)

* Irrigation Zone Controller ISY Program

![Program](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/master/Images/program1.png)

* Irrigation Zone Controller Alarm and ShutDown ISY Program

![Program](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/master/Images/Alarm%20and%20shutdown1.png)

* Example program to cycle six zones On Alexa <https://youtu.be/htW2vVqgODw>

### BASpi-SYS6U6R and the BASpi-Edge DIY BacNet Control Device by Contemporary Controls

* Main
[Contemporary Controls BASpi DIY](https://www.ccontrols.com/basautomation/baspi.htm)
* BASpi 6U6R Controller
[Contemporary Controls BASpi Edge 6U6R](https://www.ccontrols.com/basautomation/baspiedge.php)
* BASpi 6U6R Controller
[Contemporary Controls BASpi 6U6R](https://www.ccontrols.com/pdf/ds/BASPI-datasheet.pdf)
* BASpi 6U6R Installation
[Contemporary Controls BASpi 6U6R Install](https://www.ccontrols.com/pdf/BASpi-hardware-install-guide.pdf)
* BASpi 6U4R2A Controller
[Contemporary Controls BASpi 6U4R2A](https://www.ccontrols.com/pdf/ds/BASPI-AO2-datasheet.pdf)
* BASpi 6U4R2A Installation
[Contemporary Controls BASpi 6U4R2A Install](https://www.ccontrols.com/pdf/TD180600.pdf)
* BASpi Controller Configuration
[Contemporary Controls BASpi Configuration Quick Start](https://www.ccontrols.com/pdf/is/BASPI-QSGuide.pdf)

#### Future

* Need add a multiple pulldown menu for the Universal Inputs UOM's. The universal inputs have a large list of configurable UOM's of their own.
Please see configuration quick start link above. On page two it shows the GUI for the device. There you can pick on each universal input to configure its type, a seperate UOM. Also see the video below.

![Future Adds](https://github.com/sjpbailey/udi-poly-bas-irrigation-python-master/blob/master/Images/shot_3.png)

[Universal Input Configuration Video](https://www.youtube.com/watch?v=hTd1mR7npP4)

* Python 3.7.7

* Supported Nodes
  * Up to 36 Universal Inputs
  * Up to 36 Binary Outputs
  
##### Configuration

###### Defaults

* Default Short Poll:  Every 60 seconds
* Default Long Poll: Every 4 minutes (heartbeat)

###### Requirments

* requests 2.25.0
* bascontrolns  0.0.3
* polyinterface 2.1.0
* requests      2.25.0

###### User Provided

* Enter your IP address for your BASpi-SYS6U6R controllers as,
* Zone Controller 1 Config: key = irr1_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 2 Config: Key = irr2_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 3 Config: key = irr3_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 4 Config: Key = irr4_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 5 Config: key = irr5_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 6 Config: Key = irr6_ip, Value = Enter Your BASpi IP Address.
* Save and restart the NodeServer
* sjb / gtb Nov 2020
