"""Random MAC address generation utilities."""

import random
from enum import Enum


class HexValuesLength(Enum):
    """Defines the length of different MAC address components."""
    MAC_ADDRESS = 12  # Full MAC address (6 bytes = 12 hex chars)
    OUI = 6           # Organizationally Unique Identifier (3 bytes)
    NIC = 6           # Network Interface Controller specific (3 bytes)


def generate_hex_values_delimited_by_dotted(hex_values_to_generate: HexValuesLength) -> str:
    """Generate a random hex string formatted as MAC address octets.
    
    Args:
        hex_values_to_generate: Number of hex characters to generate
        
    Returns:
        Random hex string delimited by colons (e.g., "01:bf:e2")
    """
    hex_chars = [
        format(random.randint(0, 15), "x") 
        for _ in range(hex_values_to_generate.value)
    ]
    
    # Join every 2 hex chars with colons
    octets = ["".join(hex_chars[i:i + 2]) for i in range(0, len(hex_chars), 2)]
    return ":".join(octets)


def get_random_vendor_from_list(vendors: list[str]) -> str:
    """Select a random vendor OUI from a list.
    
    Args:
        vendors: List of vendor OUI strings
        
    Returns:
        A randomly selected vendor OUI
    """
    return random.choice(vendors)


def _random_byte() -> int:
    """Generate a random byte value (0-255)."""
    return random.randint(0x00, 0xFF)


def generate_safe_unicast_mac() -> str:
    """Generate a valid, locally administered unicast MAC address.
    
    The returned MAC address has:
    - Bit 1 of first byte set to 1 (locally administered)
    - Bit 0 of first byte set to 0 (unicast)
    
    These settings ensure compatibility with virtual and dummy network 
    interfaces where global or multicast MACs may be rejected by the kernel.
    
    Returns:
        MAC address string in format 'xx:xx:xx:xx:xx:xx'
    """
    first_byte = _random_byte()
    # Set locally administered bit (bit 1) and clear multicast bit (bit 0)
    first_byte = (first_byte & 0b11111100) | 0b00000010
    
    mac_bytes = [first_byte] + [_random_byte() for _ in range(5)]
    return ":".join(f"{byte:02x}" for byte in mac_bytes)
