import pytest

from logger_kit import Logger
from logger_kit.handlers import FileHandler, RotatingFileHandler


@pytest.fixture
def logger():
    return Logger(name="test_logger", level="DEBUG")


def test_basic_logging(logger, caplog):
    message = "Test message"
    logger.info(message)
    assert message in caplog.text


def test_structured_logging(logger, caplog):
    message = "User action"
    extra = {"user_id": 123, "action": "login"}
    logger.info(message, extra=extra)
    log_entry = caplog.records[-1]
    assert message in log_entry.message
    assert log_entry.user_id == 123
    assert log_entry.action == "login"


def test_log_levels(logger, caplog):
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    assert "Debug message" in caplog.text
    assert "Info message" in caplog.text
    assert "Warning message" in caplog.text
    assert "Error message" in caplog.text
    assert "Critical message" in caplog.text


def test_context_manager(logger, caplog):
    logger.info("Before context")
    with logger.context(level="ERROR"):
        logger.info("Inside context - should not appear")
        logger.error("Inside context - should appear")
    logger.info("After context")

    assert "Before context" in caplog.text
    assert "Inside context - should not appear" not in caplog.text
    assert "Inside context - should appear" in caplog.text
    assert "After context" in caplog.text


@pytest.mark.asyncio
async def test_async_logging(logger, caplog):
    message = "Async test message"
    await logger.ainfo(message)
    assert message in caplog.text


def test_file_handler(tmp_path):
    log_file = tmp_path / "test.log"
    logger = Logger(name="file_test")
    file_handler = FileHandler(str(log_file))
    logger.logger.addHandler(file_handler.get_handler())

    test_message = "Test file logging"
    logger.info(test_message)

    assert log_file.exists()
    log_content = log_file.read_text()
    assert test_message in log_content


def test_rotating_file_handler(tmp_path):
    log_file = tmp_path / "rotating.log"
    logger = Logger(name="rotating_test")
    rotating_handler = RotatingFileHandler(
        str(log_file),
        max_bytes=100,
        backup_count=3,
    )
    logger.logger.addHandler(rotating_handler.get_handler())

    # Write enough logs to trigger rotation
    for i in range(10):
        logger.info(f"Test rotating log message {i}" * 5)

    # Check that backup files were created
    assert log_file.exists()
    assert (tmp_path / "rotating.log.1").exists()
