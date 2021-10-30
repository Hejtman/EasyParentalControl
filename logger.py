import sys
import logging
from pathlib import Path


class TerminalLogger:
    def __init__(self, file_path: str):
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.file_handler = logging.FileHandler(file_path)
        self.terminal_handler = logging.StreamHandler(sys.stdout)

        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(file_formatter)
        self.file_handler.setLevel(logging.DEBUG)
        self.terminal_handler.setLevel(logging.INFO)            # default settings

        root_logger = logging.getLogger()                       # should be done only once
        root_logger.setLevel(logging.NOTSET)                    # delegate all messages
        root_logger.addHandler(self.file_handler)
        root_logger.addHandler(self.terminal_handler)

        sys.excepthook = self._log_unhandled_exception

    def __getattr__(self, attr):
        return getattr(self.logger, attr)

    def stop_logging_to_terminal(self):
        root_logger = logging.getLogger()
        root_logger.removeHandler(self.terminal_handler)

    def set_terminal_logging(self, verbosity: int):
        self.terminal_handler.setLevel(level=logging.DEBUG if verbosity >= 3 else logging.INFO)

    def _log_unhandled_exception(self, exc_type, exc_value, exc_traceback):
        self.logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
