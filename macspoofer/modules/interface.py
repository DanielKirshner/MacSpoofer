"""Network interface management for MAC spoofing."""

import contextlib
import os
from collections.abc import AsyncIterator
from enum import StrEnum

from macspoofer.utils import shell_utils
from macspoofer.utils.exceptions import CustomException, ErrorCode

SYSFS_NET_PATH = "/sys/class/net"


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

        Raises:
            CustomException: If the interface does not exist
        """
        if not os.path.exists(f"{SYSFS_NET_PATH}/{name}"):
            raise CustomException(
                message=f"Network interface '{name}' does not exist",
                error_code=ErrorCode.INTERFACE_NOT_FOUND,
            )
        self.name = name

    async def set_state(self, state: InterfaceState) -> None:
        """Set the interface to the specified state.

        Args:
            state: Desired interface state (UP or DOWN)

        Raises:
            CustomException: If the state change fails
        """
        try:
            await shell_utils.execute_command(["ip", "link", "set", "dev", self.name, state])
        except CustomException as err:
            raise CustomException(
                message=f"Failed to set interface {self.name} to {state}",
                error_code=ErrorCode.INTERFACE_STATE_FAILED,
            ) from err

    async def up(self) -> None:
        """Bring the interface up."""
        await self.set_state(InterfaceState.UP)

    async def down(self) -> None:
        """Bring the interface down."""
        await self.set_state(InterfaceState.DOWN)

    def read_mac_address(self) -> str | None:
        """Read the interface's current MAC address from sysfs.

        Returns:
            The MAC address in lowercase, or None if it could not be read
        """
        try:
            with open(f"{SYSFS_NET_PATH}/{self.name}/address", encoding="utf-8") as address_file:
                return address_file.read().strip().lower()
        except OSError:
            return None

    async def set_mac_address(self, mac: str) -> None:
        """Set the MAC address of the interface.

        Note: The interface should be down before changing the MAC address.

        The change is verified by reading the address back, because some drivers
        exit zero while silently keeping the original address.

        Args:
            mac: New MAC address (format: 'xx:xx:xx:xx:xx:xx')

        Raises:
            CustomException: If setting the MAC address fails, or if the
                interface still reports its previous address afterwards
        """
        try:
            await shell_utils.execute_command(
                ["ip", "link", "set", "dev", self.name, "address", mac]
            )
        except CustomException as err:
            raise CustomException(
                message=f"Failed to set MAC address {mac} on {self.name}",
                error_code=ErrorCode.MAC_SPOOF_FAILED,
            ) from err

        current_mac = self.read_mac_address()
        if current_mac is not None and current_mac != mac.lower():
            raise CustomException(
                message=(
                    f"Interface {self.name} still reports {current_mac} after setting {mac}; "
                    "the driver accepted the command but did not apply the change"
                ),
                error_code=ErrorCode.MAC_SPOOF_NOT_APPLIED,
            )

    @contextlib.asynccontextmanager
    async def disable_temporarily(self) -> AsyncIterator[None]:
        """Async context manager to temporarily bring the interface down and back up.

        If bringing the interface back up fails, the interface is left down and
        the user has no connectivity, so that failure takes over the reported
        error, but it carries the original body failure along in its message
        instead of hiding it.

        Usage:
            async with interface.disable_temporarily():
                await interface.set_mac_address(new_mac)

        Raises:
            CustomException: If the interface cannot be brought back up
        """
        await self.down()

        body_error: BaseException | None = None
        try:
            yield
        except BaseException as err:
            body_error = err
            raise
        finally:
            try:
                await self.up()
            except CustomException as restore_err:
                message = (
                    f"Interface {self.name} was left DOWN and could not be brought back up. "
                    f"Restore it manually with: ip link set dev {self.name} up"
                )
                if body_error is not None:
                    message += f"\nThe failure that triggered this was: {body_error}"
                raise CustomException(
                    message=message,
                    error_code=ErrorCode.INTERFACE_RESTORE_FAILED,
                ) from restore_err

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"NetworkInterface({self.name!r})"
