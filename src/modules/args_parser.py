import argparse

VERSION = "0.0.0"


class ArgumentParser:
    """Handles command line argument parsing"""
    
    def __init__(self):
        self._parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="MAC Address Spoofer - Change your network interface MAC address",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        self._add_arguments(parser)
        return parser
    
    def _add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-i',
            required=True,
            help='Network interface name (e.g., wlan0, eth0)'
        )
        
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Non-interactive mode: generate and apply a safe random unicast MAC address'
        )
        
        parser.add_argument(
            '--ci',
            action='store_true',
            help='CI mode: for automated testing (similar to --auto but with different output)'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version=f'MAC Address Spoofer v{VERSION}'
        )
    
    def parse_args(self):
        """Parse command line arguments."""
        return self._parser.parse_args()
