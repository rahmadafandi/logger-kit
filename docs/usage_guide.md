# Logger Kit Usage Guide

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- Poetry (recommended) or pip for package management

### Installation Steps

```bash
# Using Poetry (recommended)
poetry add logger-kit

# Using pip
pip install logger-kit
```

## Basic Usage

### Simple Logging

```python
from logger_kit import BaseLogger

# Initialize logger
logger = BaseLogger(name="myapp", level="INFO")

# Basic logging
logger.info("Application started")
logger.warning("Resource running low")
logger.error("Failed to connect to database")
```

### Structured Logging

```python
# Log with additional context
logger.info(
    "User registration successful",
    extra={
        "user_id": "user123",
        "email": "user@example.com",
        "registration_source": "web"
    }
)

# Log with error details
logger.error(
    "Payment processing failed",
    extra={
        "transaction_id": "tx_123",
        "amount": 99.99,
        "currency": "USD",
        "error_code": "INVALID_CARD"
    }
)
```

## Advanced Features

### File Logging

```python
from logger_kit.handlers import FileHandler, RotatingFileHandler

# Simple file logging
file_handler = FileHandler("app.log")
logger.logger.addHandler(file_handler.get_handler())

# Rotating file logging
rotating_handler = RotatingFileHandler(
    filename="app.log",
    max_bytes=5*1024*1024,  # 5MB
    backup_count=3
)
logger.logger.addHandler(rotating_handler.get_handler())
```

### Data Masking

```python
from logger_kit.masking import KeyMasker

# Create masker
masker = KeyMasker()

# Add masking patterns
masker.add_pattern("password", "*****")
masker.add_pattern("credit_card", "XXXX-XXXX-XXXX-{last4}")
masker.add_pattern("email", "{username}@*****")

# Log with masked data
user_data = {
    "username": "john_doe",
    "password": "secret123",
    "credit_card": "1234-5678-9012-3456",
    "email": "john.doe@example.com"
}

masked_data = masker.mask(user_data)
logger.info("User data", extra={"user_data": masked_data})
```

### Async Logging

```python
import asyncio

async def process_user(user_id: str):
    # Async logging
    await logger.ainfo(
        "Processing user",
        extra={"user_id": user_id, "status": "processing"}
    )
    
    # Simulate some async work
    await asyncio.sleep(1)
    
    await logger.ainfo(
        "User processed",
        extra={"user_id": user_id, "status": "completed"}
    )

# Run async function
asyncio.run(process_user("user123"))
```

### Context Management

```python
# Temporary debug logging
with logger.context(level="DEBUG"):
    logger.debug("Detailed debug information")
    logger.debug("More debug info", extra={"detail": "value"})

# Debug logging is disabled outside the context
logger.debug("This won't be logged")
```

## Best Practices

1. **Use Appropriate Log Levels**
   - DEBUG: Detailed information for debugging
   - INFO: General operational events
   - WARNING: Unexpected but handled situations
   - ERROR: Error events that might still allow the application to continue
   - CRITICAL: Very severe error events that might cause the application to terminate

2. **Structured Logging**
   - Always include relevant context in the `extra` parameter
   - Use consistent key names across your application
   - Include timestamps and request IDs for tracking

3. **Sensitive Data**
   - Always use data masking for sensitive information
   - Never log passwords, tokens, or credentials
   - Mask personal identifiable information (PII)

4. **Performance**
   - Use async logging in async applications
   - Configure appropriate log rotation settings
   - Monitor log file sizes

5. **Maintenance**
   - Regularly review and clean up logs
   - Set up log rotation to manage disk space
   - Archive old logs for compliance if needed