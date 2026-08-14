"""Traceback formatting configuration."""

from rich.traceback import install


def configure_tracebacks() -> None:
    """Install rich as the handler for uncaught exception tracebacks.

    Shows local variable values and three lines of surrounding context per
    frame, for better error readability.
    """
    install(show_locals=True, extra_lines=3)
