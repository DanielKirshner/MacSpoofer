from typing import List
from enum import Enum
import random

class HexValuesLength(Enum):
    MAC_ADDRESS = 12
    OUI = 6
    NIC = 6


@staticmethod
def generate_hex_values_delimited_by_dotted(hex_values_to_generate: HexValuesLength) -> str:
    """
        Return a random string of hex values delimited by dotted,
        as the format of a mac address or a part of it.

        Args:
            hex_values_to_generate (int): Number of values to generate

        Returns:
            str: Random hex string (for example : "01:bf:e2")
    """
    mac = ''
    
    for i in range(hex_values_to_generate.value):
        mac += hex(random.randint(0, 16))[-1].lower()
    
    MAC_DELIMITER = ':'
    mac = MAC_DELIMITER.join([mac[i:i + 2] for i in range(0, len(mac), 2)])
    
    return mac


@staticmethod
def get_random_vendor_from_list(vendors: List[str]) -> str:
    return random.choice(vendors)


def rand_byte():
    return random.randint(0x00, 0xFF)

@staticmethod
def generate_safe_unicast_mac() -> str:
    """
    Generate a valid, randomly generated MAC address.

    The returned MAC address is:
    - Locally administered (bit 1 of the first byte is set to 1)
    - Unicast (bit 0 of the first byte is set to 0)

    These settings ensure compatibility with virtual and dummy network interfaces
    where global or multicast MACs may be rejected by the kernel.

    Returns:
        str: A MAC address string in the format 'xx:xx:xx:xx:xx:xx'
    """
    first_byte = rand_byte()
    first_byte = (first_byte & 0b11111100) | 0b00000010
    mac = [first_byte] + [rand_byte() for _ in range(5)]
    return ':'.join(f"{b:02x}" for b in mac)
