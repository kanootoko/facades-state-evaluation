"""
Database enumeration types are defined here.
"""
from enum import Enum


class PTEnum(Enum):
    """\
    Photo type enumeration
    """

    DEFECT = "DEFECT"
    CLOSE_RANGE = "CLOSE_RANGE"
    MIDDLE_RANGE = "MIDDLE_RANGE"
    WIDE_RANGE = "WIDE_RANGE"


class MFEnum(Enum):
    """
    Mark feedback enumeration
    """

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    COMPLAINT = "COMPLAINT"
