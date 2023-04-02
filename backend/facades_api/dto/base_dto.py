# pylint: disable=too-few-public-methods
"""
Base DTO with `dict_for_insertion` method is defined here.
"""
from typing import Any


class BaseDto:
    """
    Base DTO class with `dict_for_insertion` method to return `vars(self)` without "id" key.
    """

    def dict_for_insertion(self) -> dict[str, Any]:
        """
        Return `vars(self)` without null values.
        """
        res = {name: value for name, value in vars(self).items() if value is not None}
        return res
