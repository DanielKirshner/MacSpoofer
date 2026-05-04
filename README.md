# MAC Address Spoofer

![CI (master)](https://github.com/DanielKirshner/MacSpoofer/actions/workflows/linux-ci.yml/badge.svg?branch=master)
![PyPI Version](https://img.shields.io/pypi/v/macspoofer)
![PyPI Downloads](https://img.shields.io/pypi/dm/macspoofer)

A command-line tool to spoof your network interface's MAC address on Linux systems.

![MacSpoofer Demo](https://raw.githubusercontent.com/DanielKirshner/MacSpoofer/master/demo/demo.gif)

## What is a MAC Address?

A **Media Access Control (MAC) address** is a unique identifier assigned to a network interface controller (NIC) for use as a network address in communications within a network segment. This identifier is used in most IEEE 802 networking technologies, including Ethernet, Wi-Fi, and Bluetooth.

Changing your MAC address can be useful for:
- **Privacy** - Prevent tracking across networks
- **Testing** - Simulate different network devices
- **Bypassing restrictions** - Some networks filter by MAC address

## MAC Address Structure

A MAC address is a **12-digit hexadecimal number** (6 bytes), typically represented in colon-hexadecimal notation (e.g., `00:1A:2B:3C:4D:5E`).

| Bytes | Name | Description |
|-------|------|-------------|
| First 3 bytes | **OUI** (Organizationally Unique Identifier) | Identifies the manufacturer |
| Last 3 bytes | **NIC** (Network Interface Controller) | Device-specific identifier |

## Features

- 🎲 **Random MAC generation** - Generate safe, locally-administered unicast addresses
- 🏭 **Vendor spoofing** - Mimic devices from Samsung, Apple, Intel, Microsoft, Huawei, Google, or Cisco
- 🖥️ **Interactive TUI** - Easy to use text interface
- ⚡ **Auto mode** - Non-interactive operation for scripts
- 🔧 **CI mode** - Designed for automated testing pipelines

## Compatibility

The tool is compatible with **Linux distributions only**.

Tested on:
- **Ubuntu** - 16.04.7, 18.04.6, 20.04.6, 22.04.5, 24.04.2
- **Debian** - 8, 9, 10, 11, 12
- **Kali** - 2021.4a, 2022.4, 2023.4, 2024.4, 2025.1
- **Raspbian** - 8, 9, 10, 11, 12

## Installation

### Via pip (recommended)

```bash
pip install macspoofer
```

### From source

```bash
chmod +x setup.sh
sudo ./setup.sh
```

## Usage

### Find Your Interface Name

```bash
ifconfig -a
# or
ip link show
```

### Interactive Mode (TUI)

```bash
sudo -E macspoofer -i <interface>
# or
sudo -E python3 main.py -i <interface>
```

### Auto Mode (Non-Interactive)

```bash
sudo -E macspoofer -i <interface> --auto
# or
sudo -E python3 main.py -i <interface> --auto
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-i <interface>` | Network interface name (e.g., `wlan0`, `eth0`) **[Required]** |
| `--auto` | Non-interactive mode: generate and apply a random unicast MAC |
| `--ci` | CI mode: for automated testing |
| `--help` | Show help message and usage examples |
| `--version` | Show version information |

### Programmatic Usage

You can also use `macspoofer` as a Python library:

#### Generate a Random MAC Address

```python
from macspoofer.utils.random_utils import generate_safe_unicast_mac

mac = generate_safe_unicast_mac()
print(mac)  # e.g. "a6:3f:12:cb:90:01"
```

#### Search & Browse Vendors

```python
from macspoofer.utils.vendors import VendorRegistry

# Total vendors in the database
print(VendorRegistry.vendor_count())

# Search by name (case-insensitive)
results = VendorRegistry.search("Raspberry")
print(results)

# Get OUI prefixes for a specific vendor
ouis = VendorRegistry.get_ouis_for_vendor("Apple")
print(ouis[:3])  # ['58:e6:ba', '8c:98:6b', ...]
```

#### Generate a Vendor-Specific MAC

```python
from macspoofer.spoofer import generate_mac_for_vendor

mac = generate_mac_for_vendor("Samsung")
print(mac)  # e.g. "e4:7a:11:2f:c8:5d"
```

#### Spoof an Interface (requires root)

```python
import asyncio
from macspoofer.modules.interface import NetworkInterface
from macspoofer.spoofer import spoof_mac_address
from macspoofer.utils.random_utils import generate_safe_unicast_mac

async def main():
    interface = NetworkInterface("wlan0")
    mac = generate_safe_unicast_mac()
    await spoof_mac_address(interface, mac, require_confirmation=False)

asyncio.run(main())
```

## License

[MIT License](LICENSE)

---

**© 2022-2026 Daniel Kirshner. All rights reserved.**