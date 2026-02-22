"""Shell command utilities for system-level operations."""

import getpass
import subprocess

from rich import print


def check_for_admin() -> bool:
    """Check if the current user has root/admin privileges.
    
    Returns:
        True if running as root, False otherwise
    """
    return getpass.getuser() == "root"


def execute_command(command_args: list[str]) -> bool:
    """Execute a shell command and return success status.
    
    Args:
        command_args: List of command arguments to execute
        
    Returns:
        True if command executed successfully (exit code 0), False otherwise
    """
    if not command_args:
        print("[bold red]No command args given.")
        return False
    
    result = subprocess.call(command_args)
    
    if result != 0:
        print(f"[bold red]Command failed with args {command_args}.")
        return False
    
    return True
