"""Shell command utilities for system-level operations."""

import asyncio
import getpass

from macspoofer.utils.exceptions import CustomException, ErrorCode


def check_for_admin() -> bool:
    """Check if the current user has root/admin privileges.

    Returns:
        True if running as root, False otherwise
    """
    return getpass.getuser() == "root"


async def execute_command(command_args: list[str]) -> None:
    """Execute a shell command asynchronously.

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

    process = await asyncio.create_subprocess_exec(
        *command_args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_output = stderr.decode().strip() if stderr else ""
        raise CustomException(
            message=f"Command failed (exit {process.returncode}): {' '.join(command_args)}"
            + (f"\n{error_output}" if error_output else ""),
            error_code=ErrorCode.COMMAND_EXECUTION_FAILED,
        )
