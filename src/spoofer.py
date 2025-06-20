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
    print(f"[bold yellow]About to turn {interface} DOWN.")
    if user_confirm_iw_down:
        input("Press Enter to continue or Ctrl+C to terminate -> ")
    print(f"\n[bold yellow]Turning {interface} OFF...")
    sleep(1)
    
    interface_set_successfully = set_interface_state(interface, InterfaceState.DOWN)
    if not interface_set_successfully:
        return
    
    print(f"[bold yellow]Spoofing {interface} mac...")
    sleep(1)
    mac_spoofed_successfully = shell_utils.execute_command(['ip', 'link', 'set', 'dev', interface, 'address', mac])
    if not mac_spoofed_successfully:
            print(f"[bold red]Failed spoofing {interface} mac address to {mac}.")
    sleep(1)
    print(f"[bold yellow]Turning {interface} back ON...")
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
    print("Generating random mac according to your request...\n")
    sleep(1)
    mac = ""
    if vendor == VENDORS[0]:
        mac = generate_hex_values_delimited_by_dotted(HexValuesLength.MAC_ADDRESS)
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
        PrettyErrorsHandle()
        run_spoofer_logic()
    except KeyboardInterrupt:
        print("[bold red]\nStopped.")
    except ModuleNotFoundError:
        print("[bold red]\nMissing one of the pip packages.")
    except Exception:
        print("[bold red]\nError occurred.")


if __name__ == "__main__":
    if shell_utils.check_for_admin() == False:
        print("[bold red]Needs root.")
        sys.exit(1)
        
    if len(sys.argv) < ArgsIndex.EXPECTED_LENGTH.value:
        print("[bold red]Missing arguments.\nAbort.")
        sys.exit(1)

    interface = sys.argv[ArgsIndex.INTERFACE.value]
    if "--ci" in sys.argv:
        unicast_mac_virtual_interface = generate_safe_unicast_mac() 
        print(f"[CI] Spoofing {interface} to {unicast_mac_virtual_interface}")
        spoof_new_mac_address(interface, unicast_mac_virtual_interface, user_confirm_iw_down=False)
    elif "--auto" in sys.argv:
        print("[AUTO] Generating safe random unicast MAC address...")
        auto_mac = generate_safe_unicast_mac()
        print(f"[AUTO] Spoofing {interface} to {auto_mac}")
        spoof_new_mac_address(interface, auto_mac, user_confirm_iw_down=False)
    else:
        main()
