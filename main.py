#!/usr/bin/env python3
"""MAC Address Spoofer - Entry point."""

from rich import print

from src.modules.args_parser import ArgumentParser
from src.modules.error_config import configure_pretty_errors
from src.spoofer import run_spoofer_logic
from src.utils.exceptions import CustomException


def main() -> None:
    """Application entry point."""
    try:
        configure_pretty_errors()
        args = ArgumentParser().parse_args()
        run_spoofer_logic(args)
    except KeyboardInterrupt:
        print("\n[-] [bold red]Stopped.")
    except CustomException as e:
        print(f"\n[-] [bold red]{e}")
    except ModuleNotFoundError:
        print("\n[-] [bold red]Missing one of the pip packages.")
    except Exception as e:
        print(f"\n[-] [bold red]Error occurred: {e}")


if __name__ == "__main__":
    main()
