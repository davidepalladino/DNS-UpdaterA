import datetime
import logging


class Logger(object):
    """
    A custom logger class that provides static methods for logging messages
    at different severity levels (INFO, WARNING, ERROR, CRITICAL).  It
    outputs messages to both the console and the Python logging system.
    """

    @staticmethod
    def info(message: str) -> None:
        """
        A custom logger class that provides static methods for logging messages
        at different severity levels (INFO, WARNING, ERROR, CRITICAL).  It
        outputs messages to both the console and the Python logging system.

        Note: This logger currently uses `logging.error` for all logging levels.
              This should be adjusted to the appropriate logging level (e.g.,
              `logging.info`, `logging.warning`, etc.) for a production
              environment.  See the TODO in the code for more details.
        """
        logging.info(message)
        Logger._print_screen("INFO", message)

    @staticmethod
    def warning(message: str) -> None:
        """
        Logs a WARNING level message.

        Args:
            message: The message to log (string).
        """
        logging.warning(message)
        Logger._print_screen("WARNING", message)

    @staticmethod
    def error(message: str) -> None:
        """
        Logs an ERROR level message.

        Args:
            message: The message to log (string).
        """
        logging.error(message)
        Logger._print_screen("ERROR", message)

    @staticmethod
    def critical(message: str) -> None:
        """
        Logs a CRITICAL level message.

        Args:
            message: The message to log (string).
        """
        logging.critical(message)
        Logger._print_screen("CRITICAL", message)

    @staticmethod
    def _print_screen(prefix: str, message: str) -> None:
        """
        Prints the log message to the console with a timestamp and prefix.

        Args:
            prefix: The log level prefix (e.g., "INFO", "ERROR") (string).
            message: The message to print (string).
        """
        print(f"[{datetime.datetime.now()}] - {prefix}: {message}")