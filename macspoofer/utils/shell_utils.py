"""Shell command utilities for system-level operations."""

import asyncio
import os
import sys

from macspoofer.utils.exceptions import CustomException, ErrorCode


def check_for_linux() -> bool:
    """Check if the current platform is Linux.

    Every system facility this tool relies on is Linux-specific:
    ``/sys/class/net`` for interface discovery, ``ip`` from iproute2 for the
    actual changes, and ``os.geteuid`` for the privilege check (which does not
    exist on Windows at all).

    Returns:
        True if running on Linux, False otherwise
    """
    return sys.platform.startswith("linux")


def check_for_admin() -> bool:
    """Check if the current process has root/admin privileges.

    Uses the effective user ID rather than the username, so it stays correct
    under ``sudo -E`` (which preserves ``$USER``/``$LOGNAME`` for the original
    caller even though the process runs as root).

    Returns:
        True if running as root, False otherwise
    """
    return os.geteuid() == 0


async def execute_command(command_args: list[str]) -> None:
    """Execute a shell command asynchronously.

    Args:
        command_args: List of command arguments to execute

    Raises:
        ValueError: If command_args is empty (a programming error, not a
            runtime failure)
        CustomException: If the executable is unavailable or the command
            exits non-zero
    """
    if not command_args:
        raise ValueError("execute_command called with no arguments")

    try:
        process = await asyncio.create_subprocess_exec(
            *command_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except (FileNotFoundError, PermissionError) as err:
        raise CustomException(
            message=f"Cannot execute '{command_args[0]}': {err.strerror}",
            error_code=ErrorCode.COMMAND_NOT_FOUND,
        ) from err

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_output = stderr.decode().strip() if stderr else ""
        raise CustomException(
            message=f"Command failed (exit {process.returncode}): {' '.join(command_args)}"
            + (f"\n{error_output}" if error_output else ""),
            error_code=ErrorCode.COMMAND_EXECUTION_FAILED,
        )
