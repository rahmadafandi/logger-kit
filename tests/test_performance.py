import asyncio
import time

import pytest

from logger_kit import Logger


@pytest.fixture
def logger():
    return Logger(name="benchmark", level="INFO")


def test_simple_logging_performance(logger, benchmark):
    def log_message():
        logger.info("Simple log message")

    benchmark(log_message)


def test_structured_logging_performance(logger, benchmark):
    def log_structured():
        logger.info(
            "Structured log message",
            extra={"user_id": 123, "action": "test", "timestamp": time.time()},
        )

    benchmark(log_structured)


def test_masked_logging_performance(logger, benchmark):
    logger.key_masker.add_exact_match("password")
    logger.key_masker.add_pattern("email", r"[^@]+@[^@]+\.[^@]+")

    def log_masked():
        logger.info(
            "Masked log message",
            extra={
                "user": {
                    "email": "test@example.com",
                    "password": "secret123",
                }
            },
        )

    benchmark(log_masked)


@pytest.mark.asyncio
async def test_async_logging_performance(logger, benchmark):
    async def log_async():
        await logger.ainfo("Async log message", extra={"task_id": 123})

    def run_async():
        loop = asyncio.get_running_loop()
        task = None
        try:
            future = log_async()
            task = loop.create_task(future)
            loop.run_until_complete(task)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if task and not task.done():
                task.cancel()

    benchmark(run_async)


def test_bulk_logging_performance(logger, benchmark):
    def log_bulk():
        for _ in range(100):
            logger.info("Bulk log message", extra={"iteration": _})

    benchmark(log_bulk)


def test_different_log_levels_performance(logger, benchmark):
    def log_different_levels():
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

    benchmark(log_different_levels)


def test_large_data_structure_logging_performance(logger, benchmark):
    large_data = {
        "users": [
            {
                "id": i,
                "name": f"user_{i}",
                "metadata": {
                    "role": "user",
                    "active": True,
                },
            }
            for i in range(100)
        ],
        "system_info": {
            "version": "1.0.0",
            "environment": "test",
            "features": [f"feature_{i}" for i in range(50)],
        },
    }

    def log_large_data():
        logger.info(
            "Processing large data structure",
            extra={
                "data": large_data,
            },
        )

    benchmark(log_large_data)


def test_error_logging_with_traceback_performance(logger, benchmark):
    def generate_error():
        try:
            raise ValueError("Test error for benchmarking")
        except Exception as e:
            logger.error(
                "Error occurred",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "traceback": str(e.__traceback__),
                },
            )

    benchmark(generate_error)


def test_multiple_handlers_logging_performance(logger, benchmark):
    import logging
    import os

    # Add an additional file handler
    file_handler = logging.FileHandler("benchmark_test.log")
    logger.logger.addHandler(file_handler)

    def log_with_multiple_handlers():
        logger.info(
            "Testing multiple handlers",
            extra={"handler_count": len(logger.logger.handlers)},
        )

    benchmark(log_with_multiple_handlers)
    # Cleanup
    logger.logger.removeHandler(file_handler)
    file_handler.close()

    if os.path.exists("benchmark_test.log"):
        os.remove("benchmark_test.log")
