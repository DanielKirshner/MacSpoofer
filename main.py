import sys

from src.modules.pretty_errors_handler import PrettyErrorsHandler
from src.modules.args_parser import ArgumentParser
from src.spoofer import run_spoofer_logic


def main() -> None:
    try:
        PrettyErrorsHandler()
        args = ArgumentParser().parse_args()
        run_spoofer_logic(args)
    except KeyboardInterrupt:
        print("\n[-] [bold red]Stopped.")
    except ModuleNotFoundError:
        print("\n[-] [bold red]Missing one of the pip packages.")
    except Exception:
        print("\n[-] [bold red]Error occurred.")


if __name__ == "__main__":
    main()
