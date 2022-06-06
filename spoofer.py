from time import sleep
from rich import print
import subprocess
import getpass
import random
import sys


# ------ Constants ------
VERSION = '0.0.0'
VENDORS = ['Total Random', 'Samsung', 'Apple', 'Intel']

# ------- Vendors -------
SAMSUNG_VENDORS = [
    '00:21:19', '00:02:78', '00:07:ab', '00:09:18', '00:0d:ae', '00:0d:e5', '00:12:47', '00:12:fb',
    '00:13:77', '00:15:99', 'e8:50:8b', 'e8:6d:cb', 'e8:7f:6b', 'e8:93:09', 'e8:b4:c8', 'e8:e5:d6',
    'ec:10:7b', 'ec:1f:72', 'ec:7c:b6', 'ec:9b:f3', 'ec:aa:25', 'ec:e0:9b', 'f0:08:f1', 'f0:25:b7',
    'f0:39:65', 'f0:5a:09', 'f0:5b:7b', 'f0:65:ae', 'f0:6b:ca', 'f0:70:4f', 'f0:72:8c', 'dc:89:83',
    'dc:cc:e6', 'dc:cf:96', 'dc:dc:e2', 'dc:f7:56', 'e0:03:6b', 'e0:99:71', 'e0:9d:13', 'e0:aa:96',
    '78:00:9e', '78:1f:db', '78:23:27', '78:25:ad', '78:37:16', '78:40:e4', '78:46:d4', '78:47:1d'
]
APPLE_VENDORS = [
    'f8:10:93', 'f8:1e:df', 'f8:27:93', 'f8:2d:7c', 'f8:38:80', 'f8:4d:89', 'f8:4e:73', 'f8:62:14',
    'f8:66:5a', 'f8:6f:c1', 'e4:b2:fb', 'e4:c6:3d', 'e4:ce:8f', 'e4:e0:a6', 'e4:e4:ab', 'e8:04:0b',
    'e8:06:88', 'e8:1c:d8', 'e8:36:17', 'e8:5f:02', 'e8:78:65', 'e8:7f:95', 'e8:80:2e', 'e8:81:52',
    'd8:cf:9c', 'd8:d1:cb', 'd8:dc:40', 'd8:de:3a', 'dc:08:0f', 'dc:0c:5c', 'dc:2b:2a', 'dc:2b:61',
    'dc:37:14', 'dc:41:5f', 'dc:52:85', 'dc:53:92', 'dc:56:e7', 'dc:80:84', 'dc:86:d8', 'dc:9b:9c',
    '5c:97:f3', '5c:ad:cf', '5c:e9:1e', '5c:f5:da', '5c:f7:e6', '5c:f9:38', '60:03:08', '60:06:e3'
]
INTEL_VENDORS = [
    '00:d7:6d', '00:db:df', '00:e1:8c', '04:33:c2', '04:56:e5', '04:6c:59', '04:cf:4b', '04:d3:b0',
    '04:e8:b9', '04:ea:56', '04:ec:d8', '04:ed:33', '08:11:96', '08:5b:d6', '08:6a:c5', '08:71:90',
    '08:8e:90', '08:9d:f4', '08:d2:3e', '08:d4:0c', '0c:54:15', '0c:7a:15', '0c:8b:fd', '0c:91:92',
    '0c:9a:3c', '0c:d2:92', '0c:dd:24', '48:45:20', '48:51:b7', '48:51:c5', '48:68:4a', '48:89:e7',
    '48:a4:72', '48:ad:9a', '48:f1:7f', '4c:03:4f', '4c:1d:96', '4c:34:88', '4c:44:5b', '4c:77:cb',
    '4c:79:6e', 'cc:d9:ac', 'cc:f9:e4', 'd0:3c:1f', 'd0:57:7b', 'd0:7e:35', 'd0:ab:d5', 'd0:c6:37'
]

# MICROSOFT_VENDORS = []
# HUAWEI_VENDORS = []
# GOOGLE_VENDORS = []


def check_for_admin() -> bool:
    return getpass.getuser() == 'root'


def generate_random_mac_address() -> str:
    mac = ''
    for i in range(12):
        mac += hex(random.randint(0, 16))[-1].lower()
    mac = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)])
    return mac


def set_interface_state(interface: str, state: str) -> None:  # state = up/down
    subprocess.call(['ip', 'link', 'set', 'dev', interface, state])


def spoof_new_mac_address(interface: str, mac: str) -> None:
    print(f"[bold yellow]About to turn {interface} DOWN.")
    input("Press Enter to continue or Ctrl+C to terminate -> ")
    print(f"\n[bold yellow]Turning {interface} OFF...")
    sleep(1)
    set_interface_state(interface, 'down')
    print(f"[bold yellow]Spoofing {interface} mac...")
    sleep(1)
    subprocess.call(['ip', 'link', 'set', 'dev', interface, 'address', mac])
    sleep(1)
    print(f"[bold yellow]Turning {interface} back ON...")
    sleep(1)
    set_interface_state(interface, 'up')


def generate_random_6_hexs() -> str:
    mac = ''
    for i in range(6):
        mac += hex(random.randint(0, 16))[-1].lower()
    mac = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)])
    return mac


def get_random_vendor_from_list(vendors: list) -> str:
    return random.choice(vendors)


def choose_vendor() -> str:
    print_options = ''
    for i in range(len(VENDORS)):
        print_options += f"[bold green][{i}] [cyan]{VENDORS[i]}\n"
    print(f"[bold magenta]Enter your choice:\n\n{print_options}")
    user_choice = str(input('-> ').strip())
    while user_choice.isnumeric() == False or int(user_choice) >= len(VENDORS):
        user_choice = str(input('Invalid choice, try again-> ').strip())
    return VENDORS[int(user_choice)]


def print_title() -> None:
    print(
        "[bold green]"
        "\t\t\t__\n"
        " ___ _ __   ___   ___  / _| ___ _ __ \n"
        "/ __| '_ \ / _ \ / _ \| |_ / _ \ '__|\n"
        "\__ \ |_) | (_) | (_) |  _|  __/ |\n"
        "|___/ .__/ \___/ \___/|_|  \___|_|\n"
        f"    |_|\t\t\t[italic green]{VERSION}\n"
    )


def run_TUI(interface: str) -> None:
    print_title()
    vendor = choose_vendor()
    print("Generating random mac according to your request...\n")
    sleep(1)
    mac = ""
    if vendor == VENDORS[0]:
        mac = generate_random_mac_address()
    else:
        if vendor == VENDORS[1]:
            mac += get_random_vendor_from_list(SAMSUNG_VENDORS)
        elif vendor == VENDORS[2]:
            mac += get_random_vendor_from_list(APPLE_VENDORS)
        elif vendor == VENDORS[3]:
            mac += get_random_vendor_from_list(INTEL_VENDORS)
        mac = mac + ':' + generate_random_6_hexs()
    
    print(f"Spoofing your interface {interface} mac to {mac}\n")
    sleep(1)
    spoof_new_mac_address(interface, mac)
    print(f"Done.")


def main() -> None:
    if check_for_admin() == False:
        print("[bold red]Needs root.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("[bold red]You must give the interface name as an argument\nAbort.")
        sys.exit(1)
    
    if len(sys.argv) > 2:
        print("[bold red]Too many arguments given.\nAbort.")
        sys.exit(1)

    try:
        run_TUI(sys.argv[1])

    except KeyboardInterrupt:
        print("[bold red]\nStopped.")
    except ModuleNotFoundError:
        print("[bold red]\nMissing one of the pip packages.")
    except Exception:
        print("[bold red]\nError occured.")


if __name__ == "__main__":
    main()
