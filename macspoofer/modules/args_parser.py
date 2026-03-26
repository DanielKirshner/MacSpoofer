"""Command-line argument parsing for MAC Address Spoofer."""

import argparse
from dataclasses import dataclass

VERSION = "0.0.0"


@dataclass
class SpooferArgs:
    """Parsed command-line arguments for the spoofer."""

    interface: str
    auto: bool = False
    ci: bool = False


class ArgumentParser:
    """Handles command-line argument parsing."""

    def __init__(self) -> None:
        self._parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="MAC Address Spoofer - Change your network interface MAC address",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self._add_arguments(parser)
        return parser

    def _add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add all command-line arguments to the parser."""
        parser.add_argument(
            "-i",
            dest="interface",
            required=True,
            help="Network interface name (e.g., wlan0, eth0)",
        )

        parser.add_argument(
            "--auto",
            action="store_true",
            help="Non-interactive mode: generate and apply a safe random unicast MAC",
        )

        parser.add_argument(
            "--ci",
            action="store_true",
            help="CI mode: for automated testing (similar to --auto)",
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"MAC Address Spoofer v{VERSION}",
        )

    def parse_args(self) -> SpooferArgs:
        """Parse command-line arguments.

        Returns:
            SpooferArgs dataclass with parsed values
        """
        args = self._parser.parse_args()
        return SpooferArgs(
            interface=args.interface,
            auto=args.auto,
            ci=args.ci,
        )
