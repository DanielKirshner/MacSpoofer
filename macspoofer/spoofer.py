"""MAC Address Spoofer - Core spoofing logic and TUI."""

import asyncio

import art
from rich import print

from macspoofer.modules.args_parser import SpooferArgs
from macspoofer.modules.interface import NetworkInterface
from macspoofer.utils import shell_utils
from macspoofer.utils.exceptions import CustomException, ErrorCode
from macspoofer.utils.random_utils import (
    HexValuesLength,
    generate_hex_values_delimited_by_dotted,
    generate_safe_unicast_mac,
    get_random_vendor_from_list,
)
from macspoofer.utils.vendors import VendorRegistry


async def spoof_mac_address(
    interface: NetworkInterface,
    mac: str,
    require_confirmation: bool = True,
) -> None:
    """Spoof the MAC address of a network interface.

    Temporarily brings the interface down via an async context manager,
    changes its MAC address, then brings it back up.

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

    async with interface.disable_temporarily():
        print(f"\n[+] [bold green]Turning {interface} OFF...")
        await asyncio.sleep(1)

        print(f"\n[+] [bold green]Spoofing {interface} mac...")
        await asyncio.sleep(1)
        await interface.set_mac_address(mac)

    print(f"\n[+] [bold green]Turning {interface} back ON...")
    await asyncio.sleep(1)


def _search_vendor() -> str | None:
    """Interactive vendor search across the full database.

    Returns:
        Selected vendor name, or None if the user backs out.
    """
    total = VendorRegistry.vendor_count()
    print(
        f"\n[bold magenta]Search across {total:,} vendors (e.g. Raspberry Pi, Netgear, Ubiquiti):\n"
    )
    query = input("search -> ").strip()
    if not query:
        return None

    results = VendorRegistry.search(query)
    if not results:
        print("[bold red]No vendors found. Try a different search term.\n")
        return None

    oui_map = VendorRegistry.get_oui_map()
    options = "\n".join(
        f"[bold green][{i}] [cyan]{name} [dim]({len(oui_map[name])} OUIs)"
        for i, name in enumerate(results)
    )
    print(f"\n[bold magenta]Search results:\n\n{options}\n")

    user_input = input("select (or Enter to go back) -> ").strip()
    if not user_input:
        return None

    while not user_input.isdigit() or int(user_input) >= len(results):
        user_input = input("Invalid choice, try again -> ").strip()
        if not user_input:
            return None

    return results[int(user_input)]


def choose_vendor() -> str:
    """Display vendor options and get user selection.

    Shows featured vendors as numbered choices plus a search option
    that queries the full database (~19k vendors).

    Returns:
        The selected vendor name
    """
    vendors = VendorRegistry.NAMES
    search_idx = len(vendors)

    options = "\n".join(f"[bold green][{i}] [cyan]{vendor}" for i, vendor in enumerate(vendors))
    options += f"\n[bold green][{search_idx}] [yellow]Search all vendors..."
    print(f"[bold magenta]Enter your choice:\n\n{options}\n")

    user_input = input("-> ").strip()
    while True:
        if user_input.isdigit() and int(user_input) <= search_idx:
            choice = int(user_input)

            if choice == search_idx:
                result = _search_vendor()
                if result is not None:
                    return result
                print(f"[bold magenta]Enter your choice:\n\n{options}\n")
                user_input = input("-> ").strip()
                continue

            return vendors[choice]

        user_input = input("Invalid choice, try again -> ").strip()


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


async def run_tui(interface: NetworkInterface) -> None:
    """Run the text-based user interface for MAC spoofing.

    Args:
        interface: NetworkInterface instance to spoof
    """
    art.tprint("Spoofer")

    vendor = choose_vendor()
    print("[+] [bold green]Generating random mac according to your request...\n")
    await asyncio.sleep(1)

    mac = generate_mac_for_vendor(vendor)

    print(f"[+] [bold green]Spoofing your interface {interface} mac to {mac}\n")
    await asyncio.sleep(1)

    await spoof_mac_address(interface, mac)
    print("\n[+] [bold green]Done.")


async def run_spoofer_logic(args: SpooferArgs) -> None:
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
        await spoof_mac_address(interface, mac, require_confirmation=False)
    else:
        await run_tui(interface)
