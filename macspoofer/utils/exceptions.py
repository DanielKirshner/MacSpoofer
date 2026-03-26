"""Custom exceptions and error codes for MacSpoofer."""

from enum import IntEnum


class ErrorCode(IntEnum):
    FAILED_TO_CREATE_LOGGER_FOLDER = 1000
    FAILED_TO_SETUP_LOGGER = 1001
    COMMAND_EXECUTION_FAILED = 1002
    INTERFACE_STATE_FAILED = 1003
    MAC_SPOOF_FAILED = 1004


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
        return f"[Error {self._error_code}] {self._message}"

    def __repr__(self) -> str:
        return f"CustomException(message='{self._message}', error_code={self._error_code})"
