"""Colored logging configuration for rezops."""

import copy
import logging
import os
import sys

RESET = "\033[0m"
LEVEL_COLORS = {
    logging.DEBUG: "\033[36m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[1;31m",
}
LOGGER = logging.getLogger("rezops")


class ColorFormatter(logging.Formatter):
    """Format log levels with terminal colors when color output is enabled."""

    def __init__(self, use_color: bool) -> None:
        """Initialize the formatter.

        Args:
            use_color: Whether to add ANSI colors to log levels.

        Returns:
            None: Initializes the formatter.
        """
        super().__init__("%(levelname)s: %(message)s")
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record, coloring its level name when enabled.

        Args:
            record: Log record to format.

        Returns:
            The formatted log message.
        """
        if self.use_color:
            record = copy.copy(record)
            color = LEVEL_COLORS.get(record.levelno)
            if color:
                record.levelname = f"{color}{record.levelname}{RESET}"
        return super().format(record)


def configure_logging() -> bool:
    """Configure colored logging for the Rez build CLI.

    Returns:
        True when the logger is configured.
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorFormatter(use_color=sys.stderr.isatty() and "NO_COLOR" not in os.environ))
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
    return True
