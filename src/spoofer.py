from pretty_errors_handler import PrettyErrorsHandle
from random_utils import *
from vendors import *
import shell_utils
from interface import InterfaceState
from enum import Enum, auto
from rich import print
from time import sleep
import sys
import art
import argparse


def set_interface_state(interface: str, state: InterfaceState) -> bool:
    interface_set_successfully = shell_utils.execute_command(['ip', 'link', 'set', 'dev', interface, state])
    if not interface_set_successfully:
        print(f"[bold red]Failed setting {interface} {state}.\nAbort.")
        return False
    return True


def spoof_new_mac_address(interface: str, mac: str, user_confirm_iw_down: bool = True) -> None:
    """
    TODO: make the command execute async and wrap this function as a class with aenter (down, spoof, up)...
    """
    print(f"[+] [bold yellow]We need to temporarily turn OFF interface: {interface}")
    if user_confirm_iw_down:
        input("Press Enter to continue or Ctrl+C to terminate -> ")
    print(f"\n[+] [bold green]Turning {interface} OFF...")
    sleep(1)
    
    interface_set_successfully = set_interface_state(interface, InterfaceState.DOWN)
    if not interface_set_successfully:
        return
    
    print(f"\n[+] [bold green]Spoofing {interface} mac...")
    sleep(1)
    mac_spoofed_successfully = shell_utils.execute_command(['ip', 'link', 'set', 'dev', interface, 'address', mac])
    if not mac_spoofed_successfully:
            print(f"\n[-] [bold red]Failed spoofing {interface} mac address to {mac}.")
    sleep(1)
    print(f"\n[+] [bold green]Turning {interface} back ON...")
    sleep(1)
    set_interface_state(interface, InterfaceState.UP)


def choose_vendor() -> str:
    print_options = ''
    for i in range(len(VENDORS)):
        print_options += f"[bold green][{i}] [cyan]{VENDORS[i]}\n"
    print(f"[bold magenta]Enter your choice:\n\n{print_options}")
    user_choice = str(input('-> ').strip())
    while user_choice.isnumeric() == False or int(user_choice) >= len(VENDORS):
        user_choice = str(input('Invalid choice, try again-> ').strip())
    return VENDORS[int(user_choice)]


def run_tui(interface: str) -> None:
    art.tprint("Spoofer")
    vendor = choose_vendor()
    print("[+] [bold green]Generating random mac according to your request...\n")
    sleep(1)
    mac = ""
    if vendor == VENDORS[0]:
        mac = generate_safe_unicast_mac()
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
        mac += ':' + generate_hex_values_delimited_by_dotted(HexValuesLength.NIC)

    print(f"[+] [bold green]Spoofing your interface {interface} mac to {mac}\n")
    sleep(1)
    spoof_new_mac_address(interface, mac)
    print(f"\n[+] [bold green]Done.")


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="MAC Address Spoofer Tool - Change your network interface MAC address",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i wlan0                 # Interactive mode with vendor selection
  %(prog)s -i wlan0 --auto          # Non-interactive mode with random MAC
  %(prog)s -i eth0 --ci             # CI mode (for automated testing)

Supported interfaces: wlan0, eth0, enp0s3, etc.
Note: This tool requires root privileges to modify network interfaces.
        """
    )
    
    parser.add_argument(
        '-i',
        required=True,
        help='Network interface name (e.g., wlan0, eth0)'
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Non-interactive mode: generate and apply a safe random unicast MAC address'
    )
    
    parser.add_argument(
        '--ci',
        action='store_true',
        help='CI mode: for automated testing (similar to --auto but with different output)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='MAC Address Spoofer v1.0.0'
    )
    
    return parser


def run_spoofer_logic(args: argparse.Namespace) -> None:
    if not shell_utils.check_for_admin():
        print("[-] [bold red]Needs root.")
        return

    interface = args.i
    
    if args.ci:
        unicast_mac_virtual_interface = generate_safe_unicast_mac() 
        print(f"\n[CI] Spoofing {interface} to {unicast_mac_virtual_interface}")
        spoof_new_mac_address(interface, unicast_mac_virtual_interface, user_confirm_iw_down=False)
    elif args.auto:
        print("\n[AUTO] Generating safe random unicast MAC address...")
        auto_mac = generate_safe_unicast_mac()
        print(f"\n[AUTO] Spoofing {interface} to {auto_mac}")
        spoof_new_mac_address(interface, auto_mac, user_confirm_iw_down=False)
    else:
        run_tui(interface)


def main() -> None:
    try:
        PrettyErrorsHandle()
        parser = create_argument_parser()
        args = parser.parse_args()
        run_spoofer_logic(args)
    except KeyboardInterrupt:
        print("\n[-] [bold red]Stopped.")
    except ModuleNotFoundError:
        print("\n[-] [bold red]Missing one of the pip packages.")
    except Exception:
        print("\n[-] [bold red]Error occurred.")


if __name__ == "__main__":
    main()
