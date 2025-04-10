import getpass
import subprocess

@staticmethod
def check_for_admin() -> bool:
    return getpass.getuser() == 'root'


@staticmethod
def execute_command(command_args: list[any]) -> bool:
    if not command_args:
         print("No command args given.")
         return False
    
    SUCCESS_RETURN_CODE = 0
    return_code = subprocess.call(command_args)

    if return_code != SUCCESS_RETURN_CODE:
            print(f"[bold red]Command failed with args {command_args}.")
            return False
    
    return True
