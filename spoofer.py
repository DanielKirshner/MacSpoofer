from rich import print
import getpass


VERSION = "0.0.0"


def print_title() -> None:
    print(
        "[bold green]"
        "\t\t\t__\n"
        " ___ _ __   ___   ___  / _| ___ _ __ \n"
        "/ __| '_ \ / _ \ / _ \| |_ / _ \ '__|\n"
        "\__ \ |_) | (_) | (_) |  _|  __/ |\n"
        "|___/ .__/ \___/ \___/|_|  \___|_|\n"
        "    |_|\n"
    )



def check_for_admin() -> bool:
    return getpass.getuser() == 'root'

def main() -> None:
    print_title()

if __name__ == "__main__":
    main()
