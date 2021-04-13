# Universal Devices BAS Irrigation Network

## BASpi-SYS6U6R DIY BacNet Control Device by Contemporary Controls

### The purpose of this Nodeserver is for custom control of BASpi modules on a network

* The purpose of this Nodeserver is for Irrigation and home automation using BASpi modules on an IP network.
* Python 3.7.7

* Supported Nodes
  * Inputs
  * Outputs
  * Multiple Modules
  
#### Configuration

##### Defaults

* Default Short Poll:  Every 60 seconds
* Default Long Poll: Every 4 minutes (heartbeat)

###### User Provided

* Enter your IP address for your BASpi-SYS6U6R controller,
* Zone Controller 1 Config: key = irr1_ip Value = Enter Your BASpi IP Address.
* Zone Controller 2 Config: Key = irr2_ip Value = Enter Your BASpi IP Address.
* Zone Controller 3 Config: key = irr3_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 4 Config: Key = irr4_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 5 Config: key = irr5_ip, Value = Enter Your BASpi IP Address.
* Zone Controller 6 Config: Key = irr6_ip, Value = Enter Your BASpi IP Address.
* Save and restart the NodeServer
* sjb / gtb Nov 2020
