#!/usr/bin/env python3
"""MAC Address Spoofer - CLI entry point."""

import asyncio

from rich import print

from macspoofer.modules.args_parser import ArgumentParser
from macspoofer.modules.error_config import configure_tracebacks
from macspoofer.spoofer import run_spoofer_logic
from macspoofer.utils.exceptions import CustomException


async def _async_main() -> None:
    """Async application entry point."""
    configure_tracebacks()
    args = ArgumentParser().parse_args()
    await run_spoofer_logic(args)


def main() -> None:
    """Synchronous wrapper for the CLI entry point (used by pyproject.toml scripts).

    Only expected failures are reported as a plain message. Anything else is a
    bug, and is left to propagate so the rich traceback handler installed by
    configure_tracebacks() can show where it came from.
    """
    try:
        asyncio.run(_async_main())
    except KeyboardInterrupt:
        print("\n[-] [bold red]Stopped.")
    except CustomException as e:
        print(f"\n[-] [bold red]{e}")


if __name__ == "__main__":
    main()
