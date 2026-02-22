"""Pretty error output configuration."""

import pretty_errors


def configure_pretty_errors() -> None:
    """Configure pretty_errors for enhanced error display.
    
    Sets up formatting options for better error readability including
    separator characters, full filename display, and context lines.
    """
    pretty_errors.configure(
        separator_character="*",
        filename_display=pretty_errors.FILENAME_FULL,
        line_color=pretty_errors.RED + "> " + pretty_errors.default_config.line_color,
        lines_before=3,
        lines_after=3,
    )
