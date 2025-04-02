import pytest

from logger_kit import Logger


@pytest.fixture
def logger():
    logger = Logger(name="test_logger", level="DEBUG")
    # Add some sensitive keys to mask
    logger.key_masker.add_exact_match("password")
    logger.key_masker.add_exact_match("api_key", "[REDACTED]")
    logger.key_masker.add_pattern("email", r"[^@]+@[^@]+\.[^@]+")
    return logger


class TestExactMatchMasking:
    def test_basic_masking(self, logger, caplog):
        """Test basic exact match masking with default and custom masks."""
        extra = {
            "username": "john_doe",
            "password": "secret123",
            "api_key": "ak_test_12345",
        }
        logger.info("User credentials", extra=extra)
        log_entry = caplog.records[-1]

        assert log_entry.username == "john_doe"  # Should not be masked
        assert log_entry.password == "*****"  # Should use default mask
        assert log_entry.api_key == "[REDACTED]"  # Should use custom mask

    def test_empty_values(self, logger, caplog):
        """Test masking of empty and None values."""
        extra = {"password": "", "api_key": None}
        logger.info("Empty credentials", extra=extra)
        log_entry = caplog.records[-1]

        # Empty string should still be masked
        assert log_entry.password == "*****"
        assert (
            log_entry.api_key == "[REDACTED]"
        )  # None should be masked with custom mask


class TestPatternMasking:
    def test_basic_pattern(self, logger, caplog):
        """Test basic pattern masking for email addresses."""
        extra = {"user": {"name": "John Doe", "email": "john@example.com"}}
        logger.info("User info", extra=extra)
        log_entry = caplog.records[-1]

        assert log_entry.user["name"] == "John Doe"  # Should not be masked
        assert log_entry.user["email"] == "*****"  # Should be masked

    def test_invalid_pattern_input(self, logger, caplog):
        """Test pattern masking with invalid email format."""
        extra = {"user": {"email": "invalid-email"}}
        logger.info("Invalid email", extra=extra)
        log_entry = caplog.records[-1]

        assert (
            log_entry.user["email"] == "invalid-email"
        )  # Should not be masked as it doesn't match pattern


class TestNestedMasking:
    def test_nested_objects(self, logger, caplog):
        """Test masking in nested dictionary structures."""
        extra = {
            "user": {
                "credentials": {
                    "password": "secret123",
                    "api_key": "ak_test_12345",
                }
            }
        }
        logger.info("Nested sensitive data", extra=extra)
        log_entry = caplog.records[-1]

        assert log_entry.user["credentials"]["password"] == "*****"
        assert log_entry.user["credentials"]["api_key"] == "[REDACTED]"

    def test_mixed_nested_data(self, logger, caplog):
        """Test masking with mixed data types in nested structures."""
        extra = {
            "data": {
                "numbers": [1, 2, 3],
                "secrets": {"password": 12345, "api_key": True},
            }
        }
        logger.info("Mixed data types", extra=extra)
        log_entry = caplog.records[-1]

        assert log_entry.data["numbers"] == [1, 2, 3]  # Should not be masked
        assert (
            log_entry.data["secrets"]["password"] == "*****"
        )  # Should mask non-string types
        assert log_entry.data["secrets"]["api_key"] == "[REDACTED]"


class TestListMasking:
    def test_list_of_objects(self, logger, caplog):
        """Test masking in lists containing dictionaries."""
        extra = {
            "users": [
                {"email": "user1@example.com"},
                {
                    "email": "user2@example.com",
                },
            ]
        }
        logger.info("User list", extra=extra)
        log_entry = caplog.records[-1]

        assert all(user["email"] == "*****" for user in log_entry.users)

    def test_empty_list(self, logger, caplog):
        """Test masking with empty lists."""
        extra = {"users": []}
        logger.info("Empty user list", extra=extra)
        log_entry = caplog.records[-1]

        assert log_entry.users == []  # Should remain empty


class TestCustomMasking:
    def test_custom_default_mask(self, logger, caplog):
        """Test changing the default mask value."""
        logger.key_masker.set_default_mask("[HIDDEN]")
        logger.info(logger.key_masker.default_mask)
        extra = {"password": "secret123"}
        logger.info("Custom mask", extra=extra)
        log_entry = caplog.records[-1]

        assert log_entry.password == "[HIDDEN]"
