import asyncio
import logging
from contextlib import contextmanager
from typing import Any, Dict, Optional

from pythonjsonlogger.json import JsonFormatter

from .masking import KeyMasker
from .version import (
    __author__,
    __author_email__,
    __copyright__,
    __license__,
    __version__,
)

__all__ = [
    "BaseLogger",
    "Logger",
    "KeyMasker",
    "__version__",
    "__author__",
    "__author_email__",
    "__copyright__",
    "__license__",
]


class BaseLogger:
    """Base logger class providing core logging functionality."""

    def __init__(self, name: str = "app", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.level = getattr(logging, level.upper())
        self.logger.setLevel(self.level)

        # Create JSON formatter
        formatter = JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            json_ensure_ascii=False,
        )

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _log(
        self, level: str, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        log_method = getattr(self.logger, level.lower())
        log_method(message, extra=extra)

    def debug(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._log("DEBUG", message, extra)

    def info(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._log("INFO", message, extra)

    def warning(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._log("WARNING", message, extra)

    def error(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._log("ERROR", message, extra)

    def critical(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._log("CRITICAL", message, extra)

    async def _alog(
        self, level: str, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        await asyncio.get_event_loop().run_in_executor(
            None, self._log, level, message, extra
        )

    async def adebug(
        self, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        await self._alog("DEBUG", message, extra)

    async def ainfo(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        await self._alog("INFO", message, extra)

    async def awarning(
        self, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        await self._alog("WARNING", message, extra)

    async def aerror(
        self, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        await self._alog("ERROR", message, extra)

    async def acritical(
        self, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        await self._alog("CRITICAL", message, extra)

    @contextmanager
    def context(self, **kwargs):  # type: ignore
        """Context manager for temporary logger settings"""
        old_settings = {}
        for key, value in kwargs.items():
            if hasattr(self, key):
                old_settings[key] = getattr(self, key)
                if key == "level":
                    value = getattr(logging, value.upper())
                    self.logger.setLevel(value)
                setattr(self, key, value)

        try:
            yield self
        finally:
            for key, value in old_settings.items():
                if key == "level":
                    self.logger.setLevel(value)
                setattr(self, key, value)


class Logger(BaseLogger):
    """Enhanced logger with data masking capabilities."""

    def __init__(self, name: str = "app", level: str = "INFO"):
        super().__init__(name, level)
        self.key_masker = KeyMasker()

    def _log(
        self, level: str, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> None:
        masked_extra = self.key_masker.mask_data(extra) if extra else {}
        # Ensure masked_extra is a dictionary or None before passing to _log
        masked_extra_dict = None
        if isinstance(masked_extra, dict):
            masked_extra_dict = masked_extra
        super()._log(level, message, masked_extra_dict)
