# pylint: disable=redefined-builtin, no-name-in-module, no-self-argument
"""
Registration request is defined here.
"""
from re import compile, match

from pydantic import BaseModel, validator

email_re = compile(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
name_re = compile(r"^\w+$")
password_re = compile(r"^[\w!@#\$%\^&\*\(\)]+$")


class RegistrationRequest(BaseModel):
    """
    Request body class given as a request for user registration endpoint.
    """

    email: str
    name: str
    password: str

    @validator("email")
    def validate_email(email: str):
        """
        Validate email with regular expression.
        """
        if match(email_re, email) is None:
            raise ValueError(f"provided email address '{email}' is invalid")
        return email

    @validator("name")
    def validate_name(name: str):
        """
        Validate name with regular expression.
        """
        if match(name_re, name) is None:
            raise ValueError(f"provided name '{name}' is invalid")
        return name

    @validator("password")
    def validate_password(password: str):
        """
        validate password with regular expression.
        """
        if match(password_re, password) is None:
            raise ValueError(f"provided password '{password}' is invalid")
        return password
