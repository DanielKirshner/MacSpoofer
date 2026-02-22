# MAC Address Spoofer

![CI (master)](https://github.com/DanielKirshner/MacSpoofer/actions/workflows/linux-ci.yml/badge.svg?branch=master)

A command-line tool to spoof your network interface's MAC address on Linux systems.

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
sudo python3 main.py -i <interface>
```

### Auto Mode (Non-Interactive)

```bash
sudo python3 main.py -i <interface> --auto
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-i <interface>` | Network interface name (e.g., `wlan0`, `eth0`) **[Required]** |
| `--auto` | Non-interactive mode: generate and apply a random unicast MAC |
| `--ci` | CI mode: for automated testing |
| `--help` | Show help message and usage examples |
| `--version` | Show version information |


## Resources

- [MAC Vendor Lookup API](https://macvendors.com/) - Look up manufacturer by MAC address
- [Wireshark Vendor Database](https://github.com/wireshark/wireshark/blob/master/manuf) - Comprehensive list of known manufacturers

> 💡 Want more vendors? Feel free to open a PR to add more vendor OUIs!

## License

[MIT License](LICENSE)

---

**© 2022-2026 Daniel Kirshner. All rights reserved.**