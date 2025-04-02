import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class FileHandler:
    def __init__(
        self,
        filename: str,
        mode: str = "a",
        encoding: str = "utf-8",
    ):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handler = logging.FileHandler(filename, mode, encoding)

    def get_handler(self) -> logging.Handler:
        return self.handler


class SysLogHandler:
    def __init__(
        self,
        address: Optional[tuple] = None,
        facility: int = logging.handlers.SysLogHandler.LOG_USER,
    ):
        if address is None:
            # Default to local syslog
            address = ("localhost", 514)
        self.handler = logging.handlers.SysLogHandler(
            address=address, facility=facility
        )

    def get_handler(self) -> logging.Handler:
        return self.handler


class RotatingFileHandler:
    def __init__(
        self,
        filename: str,
        max_bytes: int = 10485760,
        backup_count: int = 5,
        encoding: str = "utf-8",
    ):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handler = logging.handlers.RotatingFileHandler(
            filename,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=encoding,
        )

    def get_handler(self) -> logging.Handler:
        return self.handler


class TimedRotatingFileHandler:
    def __init__(
        self,
        filename: str,
        when: str = "midnight",
        interval: int = 1,
        backup_count: int = 7,
        encoding: str = "utf-8",
    ):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.handler = logging.handlers.TimedRotatingFileHandler(
            filename,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding=encoding,
        )

    def get_handler(self) -> logging.Handler:
        return self.handler
