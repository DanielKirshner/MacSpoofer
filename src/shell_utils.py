import getpass


@staticmethod
def check_for_admin() -> bool:
    return getpass.getuser() == 'root'
