# Logger Kit API Reference

## Core Components

### BaseLogger

The foundation of Logger Kit, providing core logging functionality.

```python
from logger_kit import BaseLogger

logger = BaseLogger(name="app", level="INFO")
```

#### Parameters

- `name` (str): Logger name for identification (default: "app")
- `level` (str): Logging level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

#### Methods

- `debug(message: str, extra: Optional[Dict[str, Any]] = None)`
- `info(message: str, extra: Optional[Dict[str, Any]] = None)`
- `warning(message: str, extra: Optional[Dict[str, Any]] = None)`
- `error(message: str, extra: Optional[Dict[str, Any]] = None)`
- `critical(message: str, extra: Optional[Dict[str, Any]] = None)`

### Handlers

Logger Kit provides several built-in handlers for different logging outputs:

#### FileHandler

```python
from logger_kit.handlers import FileHandler

file_handler = FileHandler(
    filename="app.log",
    mode="a",  # append mode
    encoding="utf-8"
)
```

#### RotatingFileHandler

```python
from logger_kit.handlers import RotatingFileHandler

rotating_handler = RotatingFileHandler(
    filename="app.log",
    max_bytes=10485760,  # 10MB
    backup_count=5,
    encoding="utf-8"
)
```

#### TimedRotatingFileHandler

```python
from logger_kit.handlers import TimedRotatingFileHandler

timed_handler = TimedRotatingFileHandler(
    filename="app.log",
    when="midnight",
    interval=1,
    backup_count=7,
    encoding="utf-8"
)
```

#### SysLogHandler

```python
from logger_kit.handlers import SysLogHandler

syslog_handler = SysLogHandler(
    address=None,  # Defaults to local syslog
    facility=LOG_USER
)
```

### Data Masking

Logger Kit includes a powerful data masking system for protecting sensitive information:

```python
from logger_kit.masking import KeyMasker

# Create a masker instance
masker = KeyMasker()

# Add masking patterns
masker.add_pattern("password", "*****")
masker.add_pattern("credit_card", "XXXX-XXXX-XXXX-{last4}")
```

## Advanced Usage

### Async Logging

```python
async def log_async():
    await logger.ainfo("Async log message", extra={"context": "async"})
```

### Context Management

```python
with logger.context(level="DEBUG"):
    logger.debug("Temporary debug message")
```

### Structured Logging

```python
logger.info("User action", extra={
    "user_id": 123,
    "action": "login",
    "timestamp": "2024-01-20T10:30:00Z"
})
```

## Best Practices

1. Use structured logging with the `extra` parameter for better log analysis
2. Implement appropriate log levels for different environments
3. Configure handlers based on your application's needs
4. Use data masking for sensitive information
5. Leverage async logging in async applications