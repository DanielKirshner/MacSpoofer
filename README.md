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

```
chmod +x setup.sh
sudo ./setup.sh
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
* [Mac vendor lookup API](https://macvendors.com/)

* [Wireshark known vendors "manuf" file](https://github.com/wireshark/wireshark/blob/master/manuf)
    * Feel free to add more known manufactures to 'vendors.py'

## License
### MIT-License
### © 2022-2025 Daniel Kirshner. All rights reserved.