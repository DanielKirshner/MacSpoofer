from src.modules.pretty_errors_handler import PrettyErrorsHandler
from src.utils.random_utils import *
from src.utils.vendors import *
import src.utils.shell_utils as shell_utils
from src.modules.interface import InterfaceState
from enum import Enum, auto
from rich import print
from time import sleep
import sys
import art


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


def run_spoofer_logic(args) -> None:
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