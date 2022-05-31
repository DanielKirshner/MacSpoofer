# Mac Address Spoofer Tool

## What is a mac address?
A media access control address is a unique identifier assigned to a network interface controller for use as a network address in communications within a network segment. This use is common in most IEEE 802 networking technologies, including Ethernet, Wi-Fi, and Bluetooth.
We would like to change it sometimes due to security reasons.


## The structure of a mac address
Mac Address is a 12-digit hexadecimal number (6-Byte binary number), which is mostly represented by Colon-Hexadecimal notation. First 6-digits (say 00:40:96) of MAC Address identifies the manufacturer, called as OUI (Organizational Unique Identifier).


## Compatibility
The tool is currently compatible with linux distributions only.
Tested on:
- Ubuntu (16.04 - 22.04)
- Fedora (34 - 37)
- Debian (8 - 11)
- Raspbian (8 - 11)


## Setup

- Install python 3 -> https://www.python.org/
- Make sure you are using python 3.8+
```
python3 --version
```
- Download my project:
```
git clone https://github.com/DanielKirshner/MacSpoofer
```
- Navigate to the folder created:
```
cd MacSpoofer/
```
- Install pip for python3
```
sudo apt-get update
sudo apt-get install python3-pip
```
- Install pip prerequisites
```
pip install -r requirements.txt
```
- Install necessary linux packages
```
sudo apt-get install net-tools
sudo apt-get install iproute2
```


## Usage

- Check for your wifi/bluetooth/ethernet interface name:
```
ifconfig -a
```

- Run the tool as administrator with your interface name as an argument:
```
sudo python3 spoofer.py wlp03s
```

## Other tools
Mac vendor lookup API - https://macvendors.com/

Wireshark known vendors "manuf" file - https://github.com/wireshark/wireshark/blob/master/manuf

## Future updates
- Windows Support (Using registry key values)
- Mac OS support

## License
### MIT-License
### © 2022 Daniel Kirshner. All rights reserved.