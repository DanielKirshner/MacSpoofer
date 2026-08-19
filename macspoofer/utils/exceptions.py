"""Custom exceptions and error codes for MacSpoofer."""

from enum import IntEnum


class ErrorCode(IntEnum):
    """Error codes for expected MacSpoofer failures, grouped by subsystem."""

    # Shell command execution
    COMMAND_EXECUTION_FAILED = 1000
    COMMAND_NOT_FOUND = 1001

    # Environment prerequisites
    NOT_ROOT = 1002
    UNSUPPORTED_PLATFORM = 1003

    # Network interface handling
    INTERFACE_NOT_FOUND = 1004
    INTERFACE_STATE_FAILED = 1005
    INTERFACE_RESTORE_FAILED = 1006

    # MAC address spoofing
    MAC_SPOOF_FAILED = 1007
    MAC_SPOOF_NOT_APPLIED = 1008

    # Bundled data
    VENDOR_DB_LOAD_FAILED = 1009


class CustomException(Exception):
    """Base exception for MacSpoofer with an associated error code."""

    def __init__(self, message: str, error_code: ErrorCode):
        self._message = message
        self._error_code = error_code
        super().__init__(self._message)

    @property
    def error_code(self) -> ErrorCode:
        return self._error_code

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        # IntEnum stringifies to the bare number, which is useless in a bug
        # report, so spell out the name alongside it.
        return f"[Error {self._error_code.name} ({self._error_code.value})] {self._message}"

    def __repr__(self) -> str:
        return f"CustomException(message='{self._message}', error_code={self._error_code!r})"
