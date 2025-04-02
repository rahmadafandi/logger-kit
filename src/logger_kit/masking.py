import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Pattern, Union

logger = logging.getLogger(__name__)


@dataclass
class MaskingRule:
    """Represents a masking rule with pattern and mask value."""

    pattern: Optional[Pattern[str]] = None
    mask: str = "*****"


class KeyMasker:
    """Handles masking of sensitive data in logging output.

    Provides functionality for masking data
    using exact matches or regex patterns.
    Supports nested dictionaries and lists.
    """

    def __init__(self, default_mask: str = "*****"):
        self.rules: Dict[str, MaskingRule] = {}
        self.default_mask: str = default_mask

    def add_pattern(
        self,
        key: str,
        pattern: str,
        mask: Optional[str] = None,
    ) -> None:
        """Add a regex pattern to mask matching values for a specific key."""
        try:
            compiled_pattern = re.compile(pattern)
            self.rules[key] = MaskingRule(
                pattern=compiled_pattern, mask=mask or self.default_mask
            )
        except re.error as e:
            logger.error(f"Invalid regex pattern for key {key}: {e}")

    def add_exact_match(self, key: str, mask: Optional[str] = None) -> None:
        """Add a key to be masked with exact matching."""
        self.rules[key] = MaskingRule(mask=mask or self.default_mask)

    def set_default_mask(self, mask: str) -> None:
        """Set the default masking string."""
        if not mask:
            raise ValueError("Mask value cannot be empty")

        # Update mask for rules using the default mask
        for rule in self.rules.values():
            if rule.mask == self.default_mask:
                rule.mask = mask

        self.default_mask = mask

    def _mask_value(self, key: str, value: Any) -> Any:
        """Mask a single value based on configured patterns and exact matches.

        Args:
            key: The key to check for masking rules
            value: The value to potentially mask

        Returns:
            The masked value if rules apply, otherwise the original value
        """
        if not isinstance(value, (str, int, float, bool, type(None))):
            return value

        if key not in self.rules:
            return value

        rule = self.rules[key]
        str_value = str(value)

        try:
            if rule.pattern:
                return rule.pattern.sub(rule.mask, str_value)
            return rule.mask
        except Exception as e:
            logger.error(f"Error masking value for key {key}: {e}")
            return value

    def mask_data(
        self, data: Union[Dict[str, Any], List[Any], Any]
    ) -> Union[Dict[str, Any], List[Any], Any]:
        """Recursively mask sensitive data in a dictionary or list.

        Args:
            data: The dictionary or list containing data to be masked

        Returns:
            A new dictionary or list with sensitive data
            masked according to rules
        """
        # Handle None case
        if data is None:
            return None

        # Handle dictionary case
        if isinstance(data, dict):
            return {
                key: (
                    self.mask_data(value)
                    if isinstance(value, (dict, list))
                    else self._mask_value(key, value)
                )
                for key, value in data.items()
            }

        # Handle list case
        if isinstance(data, list):
            return [
                self.mask_data(val) if isinstance(val, (dict, list)) else val
                for val in data
            ]

        # Handle tuple case by converting to list and back
        if isinstance(data, tuple):
            return tuple(self.mask_data(list(data)))

        # Return unmodified data for other types
        return data
