from vendors import *
import shell_utils
from rich import print
from enum import Enum, auto
from time import sleep
import subprocess
import random
import sys


def generate_random_mac_address() -> str:
    mac = ''
    for i in range(12):
        mac += hex(random.randint(0, 16))[-1].lower()
    mac = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)])
    return mac


def set_interface_state(interface: str, state: str) -> None:  # state = up/down
    return_code = subprocess.call(['ip', 'link', 'set', 'dev', interface, state])
    if return_code != 0: # TODO: add shell utils to run command (params = command, expected_return_code)
        print(f"[bold red]Failed setting {interface} {state}.\nAbort.")
        sys.exit(1)


def spoof_new_mac_address(interface: str, mac: str) -> None:
    print(f"[bold yellow]About to turn {interface} DOWN.")
    input("Press Enter to continue or Ctrl+C to terminate -> ")
    print(f"\n[bold yellow]Turning {interface} OFF...")
    sleep(1)
    set_interface_state(interface, 'down')
    print(f"[bold yellow]Spoofing {interface} mac...")
    sleep(1)
    return_code = subprocess.call(['ip', 'link', 'set', 'dev', interface, 'address', mac])
    if return_code != 0:
            print(f"[bold red]Failed spoofing {interface} mac address to {mac}.")
    sleep(1)
    print(f"[bold yellow]Turning {interface} back ON...")
    sleep(1)
    set_interface_state(interface, 'up')


def generate_random_6_hex_values() -> str:
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
        f"    |_|\n"
    )


def run_tui(interface: str) -> None:
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
        elif vendor == VENDORS[4]:
            mac += get_random_vendor_from_list(MICROSOFT_VENDORS)
        elif vendor == VENDORS[5]:
            mac += get_random_vendor_from_list(HUAWEI_VENDORS)
        elif vendor == VENDORS[6]:
            mac += get_random_vendor_from_list(GOOGLE_VENDORS)
        elif vendor == VENDORS[7]:
            mac += get_random_vendor_from_list(CISCO_VENDORS)
        mac += ':' + generate_random_6_hex_values()

    print(f"Spoofing your interface {interface} mac to {mac}\n")
    sleep(1)
    spoof_new_mac_address(interface, mac)
    print(f"Done.")


class ArgsIndex(Enum):
    INTERFACE = auto()
    EXPECTED_LENGTH = auto()

def run_spoofer_logic() -> None:
    if shell_utils.check_for_admin() == False:
        print("[bold red]Needs root.")
        return
        
    if len(sys.argv) < ArgsIndex.EXPECTED_LENGTH.value:
        print("[bold red]Missing arguments.\nAbort.")
        return

    run_tui(sys.argv[ArgsIndex.INTERFACE.value])


def main() -> None:
    try:
        run_spoofer_logic()
    except KeyboardInterrupt:
        print("[bold red]\nStopped.")
    except ModuleNotFoundError:
        print("[bold red]\nMissing one of the pip packages.")
    except Exception:
        print("[bold red]\nError occurred.")


if __name__ == "__main__":
    main()
