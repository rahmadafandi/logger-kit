# Logger Kit

[![PyPI version](https://badge.fury.io/py/logger-kit.svg)](https://badge.fury.io/py/logger-kit)
[![Python Versions](https://img.shields.io/pypi/pyversions/logger-kit.svg)](https://pypi.org/project/logger-kit/)
[![Build Status](https://github.com/rahmadafandi/logger-kit/actions/workflows/release.yml/badge.svg)](https://github.com/rahmadafandi/logger-kit/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful and flexible logging library for Python applications that provides structured logging, filtering capabilities, custom handlers, and asynchronous support. This library helps you implement comprehensive logging with features like data masking, async support, and structured output.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data Masking](#data-masking)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Documentation

- [API Reference](docs/api_reference.md) - Detailed API documentation and method references
- [Configuration Guide](docs/configuration_guide.md) - Comprehensive configuration options and examples
- [Usage Guide](docs/usage_guide.md) - Step-by-step guide and best practices

## Features

- **Structured Logging**: JSON-formatted logs for better parsing and analysis
- **Flexible Configuration**: Easy-to-use log filtering and level management
- **Custom Handlers**: Support for custom log handlers and formatters
- **Context Management**: Temporary logging settings using context managers
- **Async Support**: Asynchronous logging for improved performance
- **Data Masking**: Advanced masking for sensitive information protection
- **Python 3.7+**: Compatible with Python 3.7 and newer versions

## Installation

Logger Kit is available on PyPI and can be installed with Poetry:

```bash
# Using Poetry (recommended)
poetry add logger-kit

# Using pip
pip install logger-kit
```

## Quick Start

```python
from logger_kit import Logger

# Create a logger instance
logger = Logger(name="app", level="INFO")

# Basic logging
logger.info("Hello, World!")

# Structured logging with additional context
logger.info("User logged in", extra={
    "user_id": 123,
    "ip": "192.168.1.1",
    "status": "success"
})

# Using context manager for temporary settings
with logger.context(level="DEBUG"):
    logger.debug("This is a debug message")

# Async logging
async def main():
    await logger.ainfo("Processing task", extra={"task_id": "123"})
    await logger.adebug("Task details", extra={"details": "..."})
```

## Data Masking

Protect sensitive information with advanced data masking:

```python
logger = Logger(name="secure_app")

# Configure masking rules
logger.key_masker.set_default_mask("[MASKED]")
logger.key_masker.add_exact_match("password")
logger.key_masker.add_exact_match("api_key", "[REDACTED]")
logger.key_masker.add_pattern("email", r"[^@]+@[^@]+\.[^@]+")

# Logging with sensitive data (will be automatically masked)
logger.info("User data", extra={
    "user": {
        "email": "user@example.com",
        "password": "secret123",
        "api_key": "ak_test_12345"
    }
})
```

## Development

1. Clone the repository:

   ```bash
   git clone https://github.com/rahmadafandi/logger-kit.git
   cd logger-kit
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

3. Run tests:
   ```bash
   poetry run pytest
   ```

## Requirements

- Python ≥ 3.9
- python-json-logger ≥ 2.0.0
- aiofiles ≥ 0.8.0

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

Please ensure your code follows our style guide and includes appropriate tests.

## Support

For support, please:

- Open an issue on GitHub
- Contact us at rahmadafandiii@gmail.com

## Author

Rahmad Afandi (rahmadafandiii@gmail.com)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
