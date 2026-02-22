"""MAC Address Spoofer - Core spoofing logic and TUI."""

from time import sleep

import art
from rich import print

from src.modules.args_parser import SpooferArgs
from src.modules.interface import NetworkInterface
from src.utils import shell_utils
from src.utils.exceptions import CustomException, ErrorCode
from src.utils.random_utils import (
    HexValuesLength,
    generate_hex_values_delimited_by_dotted,
    generate_safe_unicast_mac,
    get_random_vendor_from_list,
)
from src.utils.vendors import VendorRegistry


def spoof_mac_address(
    interface: NetworkInterface,
    mac: str,
    require_confirmation: bool = True,
) -> None:
    """Spoof the MAC address of a network interface.

    This function temporarily brings the interface down, changes its MAC address,
    and brings it back up.

    Args:
        interface: NetworkInterface instance to spoof
        mac: New MAC address to assign (format: 'xx:xx:xx:xx:xx:xx')
        require_confirmation: If True, wait for user confirmation before proceeding

    Raises:
        CustomException: If any step of the spoofing process fails
    """
    print(f"[+] [bold yellow]We need to temporarily turn OFF interface: {interface}")

    if require_confirmation:
        input("Press Enter to continue or Ctrl+C to terminate -> ")

    print(f"\n[+] [bold green]Turning {interface} OFF...")
    sleep(1)
    interface.down()

    print(f"\n[+] [bold green]Spoofing {interface} mac...")
    sleep(1)
    interface.set_mac_address(mac)

    sleep(1)
    print(f"\n[+] [bold green]Turning {interface} back ON...")
    sleep(1)
    interface.up()


def choose_vendor() -> str:
    """Display vendor options and get user selection.

    Returns:
        The selected vendor name
    """
    vendors = VendorRegistry.NAMES
    options = "\n".join(f"[bold green][{i}] [cyan]{vendor}" for i, vendor in enumerate(vendors))
    print(f"[bold magenta]Enter your choice:\n\n{options}\n")

    user_input = input("-> ").strip()

    while not user_input.isdigit() or int(user_input) >= len(vendors):
        user_input = input("Invalid choice, try again-> ").strip()

    return vendors[int(user_input)]


def generate_mac_for_vendor(vendor: str) -> str:
    """Generate a MAC address for the specified vendor.

    Args:
        vendor: Vendor name (must be in VendorRegistry.NAMES)

    Returns:
        A valid MAC address string
    """
    if vendor == VendorRegistry.NAMES[0]:
        return generate_safe_unicast_mac()

    vendor_oui_list = VendorRegistry.get_ouis_for_vendor(vendor)
    if vendor_oui_list is None:
        return generate_safe_unicast_mac()

    oui = get_random_vendor_from_list(vendor_oui_list)
    nic = generate_hex_values_delimited_by_dotted(HexValuesLength.NIC)
    return f"{oui}:{nic}"


def run_tui(interface: NetworkInterface) -> None:
    """Run the text-based user interface for MAC spoofing.

    Args:
        interface: NetworkInterface instance to spoof
    """
    art.tprint("Spoofer")

    vendor = choose_vendor()
    print("[+] [bold green]Generating random mac according to your request...\n")
    sleep(1)

    mac = generate_mac_for_vendor(vendor)

    print(f"[+] [bold green]Spoofing your interface {interface} mac to {mac}\n")
    sleep(1)

    spoof_mac_address(interface, mac)
    print("\n[+] [bold green]Done.")


def run_spoofer_logic(args: SpooferArgs) -> None:
    """Main entry point for the spoofer logic.

    Args:
        args: Parsed command-line arguments

    Raises:
        CustomException: If not running as root
    """
    if not shell_utils.check_for_admin():
        raise CustomException(
            message="This tool must be run as root (sudo)",
            error_code=ErrorCode.COMMAND_EXECUTION_FAILED,
        )

    interface = NetworkInterface(args.interface)

    if args.ci or args.auto:
        mode = "CI" if args.ci else "AUTO"
        print(f"\n[{mode}] Generating safe random unicast MAC address...")
        mac = generate_safe_unicast_mac()
        print(f"\n[{mode}] Spoofing {interface} to {mac}")
        spoof_mac_address(interface, mac, require_confirmation=False)
    else:
        run_tui(interface)
