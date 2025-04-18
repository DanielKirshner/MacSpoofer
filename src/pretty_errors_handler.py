import pretty_errors

class PrettyErrorsHandle:
    
    def __init__(self):
        pretty_errors.configure(
            separator_character = '*',
            filename_display = pretty_errors.FILENAME_FULL,
            line_color = pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
            lines_before = 3,
            lines_after = 3
        )