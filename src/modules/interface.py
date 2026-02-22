"""Network interface management for MAC spoofing."""

from enum import StrEnum

from src.utils import shell_utils
from src.utils.exceptions import CustomException, ErrorCode


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

    def set_state(self, state: InterfaceState) -> None:
        """Set the interface to the specified state.

        Args:
            state: Desired interface state (UP or DOWN)

        Raises:
            CustomException: If the state change fails
        """
        try:
            shell_utils.execute_command(["ip", "link", "set", "dev", self.name, state])
        except CustomException as err:
            raise CustomException(
                message=f"Failed to set interface {self.name} to {state}",
                error_code=ErrorCode.INTERFACE_STATE_FAILED,
            ) from err

    def up(self) -> None:
        """Bring the interface up."""
        self.set_state(InterfaceState.UP)

    def down(self) -> None:
        """Bring the interface down."""
        self.set_state(InterfaceState.DOWN)

    def set_mac_address(self, mac: str) -> None:
        """Set the MAC address of the interface.

        Note: The interface should be down before changing the MAC address.

        Args:
            mac: New MAC address (format: 'xx:xx:xx:xx:xx:xx')

        Raises:
            CustomException: If setting the MAC address fails
        """
        try:
            shell_utils.execute_command(["ip", "link", "set", "dev", self.name, "address", mac])
        except CustomException as err:
            raise CustomException(
                message=f"Failed to set MAC address {mac} on {self.name}",
                error_code=ErrorCode.MAC_SPOOF_FAILED,
            ) from err

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"NetworkInterface({self.name!r})"
