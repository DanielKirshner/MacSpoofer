#!/usr/bin/env python3
"""MAC Address Spoofer - CLI entry point."""

import asyncio

from rich import print

from macspoofer.modules.args_parser import ArgumentParser
from macspoofer.modules.error_config import configure_pretty_errors
from macspoofer.spoofer import run_spoofer_logic
from macspoofer.utils.exceptions import CustomException


async def _async_main() -> None:
    """Async application entry point."""
    try:
        configure_pretty_errors()
        args = ArgumentParser().parse_args()
        await run_spoofer_logic(args)
    except KeyboardInterrupt:
        print("\n[-] [bold red]Stopped.")
    except CustomException as e:
        print(f"\n[-] [bold red]{e}")
    except ModuleNotFoundError:
        print("\n[-] [bold red]Missing one of the pip packages.")
    except Exception as e:
        print(f"\n[-] [bold red]Error occurred: {e}")


def main() -> None:
    """Synchronous wrapper for the CLI entry point (used by pyproject.toml scripts)."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
