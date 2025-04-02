# Logger Kit Configuration Guide

## Configuration Overview

Logger Kit provides flexible configuration options to customize logging behavior for different environments and use cases.

## Basic Configuration

### Environment-based Configuration

```python
import os
from logger_kit import BaseLogger
from logger_kit.handlers import FileHandler, SysLogHandler

# Get environment settings
ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logger based on environment
def setup_logger():
    logger = BaseLogger(name="myapp", level=LOG_LEVEL)
    
    if ENV == "production":
        # Production setup
        syslog_handler = SysLogHandler()
        logger.logger.addHandler(syslog_handler.get_handler())
    else:
        # Development setup
        file_handler = FileHandler("development.log")
        logger.logger.addHandler(file_handler.get_handler())
    
    return logger
```

## Advanced Configuration

### Custom Formatter

```python
from pythonjsonlogger import jsonlogger

class CustomFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['app_name'] = 'myapp'
        log_record['environment'] = ENV
        log_record['timestamp'] = self.formatTime(record)

# Apply custom formatter
formatter = CustomFormatter(
    '%(timestamp)s %(name)s %(levelname)s %(message)s'
)
handler.setFormatter(formatter)
```

### Multiple Handlers

```python
from logger_kit.handlers import (
    FileHandler,
    RotatingFileHandler,
    TimedRotatingFileHandler,
    SysLogHandler
)

def configure_handlers(logger):
    # File handler for all logs
    file_handler = FileHandler("app.log")
    
    # Rotating handler for error logs
    error_handler = RotatingFileHandler(
        "error.log",
        max_bytes=1024*1024,  # 1MB
        backup_count=5
    )
    error_handler.get_handler().setLevel(logging.ERROR)
    
    # Timed rotating handler for audit logs
    audit_handler = TimedRotatingFileHandler(
        "audit.log",
        when="midnight",
        interval=1,
        backup_count=30
    )
    
    # Add all handlers
    logger.logger.addHandler(file_handler.get_handler())
    logger.logger.addHandler(error_handler.get_handler())
    logger.logger.addHandler(audit_handler.get_handler())
```

### Masking Configuration

```python
from logger_kit.masking import KeyMasker

def configure_masking():
    masker = KeyMasker()
    
    # Add standard patterns
    masker.add_pattern("password", "*****")
    masker.add_pattern("api_key", "api_****")
    
    # Add custom patterns
    masker.add_pattern(
        "credit_card",
        lambda x: f"XXXX-XXXX-XXXX-{x[-4:]}"
    )
    masker.add_pattern(
        "email",
        lambda x: f"{x.split('@')[0]}@*****"
    )
    
    return masker
```

## Environment Variables

Logger Kit can be configured using environment variables:

```bash
# Basic configuration
APP_ENV=production
LOG_LEVEL=INFO

# File locations
LOG_DIR=/var/log/myapp
MAIN_LOG_FILE=app.log
ERROR_LOG_FILE=error.log

# Rotation settings
MAX_LOG_SIZE=5242880  # 5MB
BACKUP_COUNT=5

# Syslog configuration
SYSLOG_HOST=localhost
SYSLOG_PORT=514
```

## Configuration Examples

### Development Environment

```python
# development_config.py
from logger_kit import BaseLogger
from logger_kit.handlers import FileHandler

def setup_development_logger():
    logger = BaseLogger(name="myapp", level="DEBUG")
    
    # Console output with detailed formatting
    handler = FileHandler("dev.log")
    formatter = CustomFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.get_handler().setFormatter(formatter)
    
    logger.logger.addHandler(handler.get_handler())
    return logger
```

### Production Environment

```python
# production_config.py
from logger_kit import BaseLogger
from logger_kit.handlers import SysLogHandler, RotatingFileHandler

def setup_production_logger():
    logger = BaseLogger(name="myapp", level="INFO")
    
    # Syslog handler for system monitoring
    syslog = SysLogHandler()
    logger.logger.addHandler(syslog.get_handler())
    
    # Rotating file handler for application logs
    file_handler = RotatingFileHandler(
        "/var/log/myapp/app.log",
        max_bytes=10*1024*1024,  # 10MB
        backup_count=10
    )
    logger.logger.addHandler(file_handler.get_handler())
    
    return logger
```

## Best Practices

1. **Environment Separation**
   - Use different configurations for development and production
   - Keep sensitive settings in environment variables
   - Use appropriate log levels for each environment

2. **Handler Configuration**
   - Configure multiple handlers for different purposes
   - Use appropriate rotation settings to manage disk space
   - Set up proper permissions for log files

3. **Formatter Configuration**
   - Use structured logging with JSON formatting
   - Include relevant metadata in log records
   - Maintain consistent formatting across handlers

4. **Security Configuration**
   - Configure proper file permissions
   - Use masking for sensitive data
   - Implement secure transport for remote logging

5. **Performance Configuration**
   - Configure appropriate buffer sizes
   - Set up log rotation to prevent disk space issues
   - Use async logging when appropriate