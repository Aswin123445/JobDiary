
import re
from app.utils.regex_patterns import STRONG_PASSWORD_REGEX

def validate_password_helper(value: str) -> str:
    pattern = re.compile(STRONG_PASSWORD_REGEX)
    if not pattern.fullmatch(value):
        raise ValueError(
            "Password must be at least 8 characters long, "
            "contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character."
        )
    return value

def validate_username_helper(value: str) -> str:
    letter_count = sum(i.isalpha() for i in value)
    if letter_count < 3:
        raise ValueError("Username must contain at least 3 letters.")
    return value