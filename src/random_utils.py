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


def get_random_vendor_from_list(vendors: List[str]) -> str:
    return random.choice(vendors)
