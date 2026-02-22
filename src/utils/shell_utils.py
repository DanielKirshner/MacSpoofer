"""Shell command utilities for system-level operations."""

import getpass
import subprocess

from src.utils.exceptions import CustomException, ErrorCode


def check_for_admin() -> bool:
    """Check if the current user has root/admin privileges.

    Returns:
        True if running as root, False otherwise
    """
    return getpass.getuser() == "root"


def execute_command(command_args: list[str]) -> None:
    """Execute a shell command.

    Args:
        command_args: List of command arguments to execute

    Raises:
        CustomException: If command_args is empty or the command exits non-zero
    """
    if not command_args:
        raise CustomException(
            message="execute_command called with no arguments",
            error_code=ErrorCode.COMMAND_EXECUTION_FAILED,
        )

    result = subprocess.call(command_args)

    if result != 0:
        raise CustomException(
            message=f"Command failed (exit {result}): {' '.join(command_args)}",
            error_code=ErrorCode.COMMAND_EXECUTION_FAILED,
        )
