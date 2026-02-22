"""Network interface management for MAC spoofing."""

from enum import StrEnum

from rich import print

from src.utils import shell_utils


class InterfaceState(StrEnum):
    """Network interface state values."""
    UP = "up"
    DOWN = "down"


class NetworkInterface:
    """Represents a network interface for MAC address manipulation.
    
    This class encapsulates operations on a network interface,
    including state management and MAC address spoofing.
    
    Attributes:
        name: The interface name (e.g., 'eth0', 'wlan0')
    """
    
    def __init__(self, name: str) -> None:
        """Initialize a NetworkInterface.
        
        Args:
            name: The interface name (e.g., 'eth0', 'wlan0')
        """
        self.name = name
    
    def set_state(self, state: InterfaceState) -> bool:
        """Set the interface to the specified state.
        
        Args:
            state: Desired interface state (UP or DOWN)
            
        Returns:
            True if the state was set successfully, False otherwise
        """
        success = shell_utils.execute_command(
            ["ip", "link", "set", "dev", self.name, state]
        )
        if not success:
            print(f"[bold red]Failed setting {self.name} {state}.\nAbort.")
        return success
    
    def up(self) -> bool:
        """Bring the interface up.
        
        Returns:
            True if successful, False otherwise
        """
        return self.set_state(InterfaceState.UP)
    
    def down(self) -> bool:
        """Bring the interface down.
        
        Returns:
            True if successful, False otherwise
        """
        return self.set_state(InterfaceState.DOWN)
    
    def set_mac_address(self, mac: str) -> bool:
        """Set the MAC address of the interface.
        
        Note: The interface should be down before changing the MAC address.
        
        Args:
            mac: New MAC address (format: 'xx:xx:xx:xx:xx:xx')
            
        Returns:
            True if successful, False otherwise
        """
        success = shell_utils.execute_command(
            ["ip", "link", "set", "dev", self.name, "address", mac]
        )
        if not success:
            print(f"[-] [bold red]Failed setting MAC address to {mac}.")
        return success
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"NetworkInterface({self.name!r})"