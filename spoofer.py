from rich import print
import subprocess
import getpass
import random
import sys


VERSION = "0.0.0"


def check_for_admin() -> bool:
    return getpass.getuser() == 'root'


def generate_random_mac_address() -> str:
    mac = ''
    for i in range(12):
        mac += hex(random.randint(0,16))[-1].lower()
    mac = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)])
    return mac


def set_interface_state(interface: str, state: str) -> None: # state = up/down
    subprocess.call(['ip', 'link', 'set', 'dev', interface, state])


def spoof_new_mac_address(interface: str, mac: str) -> None:
    set_interface_state(interface, 'down') # turn off the interface - TODO: should warn the user before
    subprocess.call(['ip', 'link', 'set', 'dev', interface, 'address', mac])
    set_interface_state(interface, 'up') # turn it back on


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


def main() -> None:
    if check_for_admin() == False:
        print("[bold red]Needs root.")
        sys.exit(0)
    
    if len(sys.argv) < 2:
        print("[bold red]You must give the interface name as an argument\nAbort.")
        sys.exit(0)
    
    try:
        print_title()
        interface = sys.argv[1] # ---- TODO: check if there are more than one argument
        new_mac = generate_random_mac_address()
        print(new_mac)
        # spoof_new_mac_address(interface, new_mac)

    except KeyboardInterrupt:
        print("[bold red]\nStopped.")
    except ModuleNotFoundError:
        print("[bold red]\nMissing one of the pip packages.")
    except Exception:
        print("[bold red]\nError occured.")


if __name__ == "__main__":
    main()
