"""MAC Address Spoofer - A CLI tool to spoof network interface MAC addresses on Linux."""

try:
    from macspoofer._version import __version__
except ModuleNotFoundError:
    __version__ = "dev"
