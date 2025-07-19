STRONG_PASSWORD_REGEX = (
    r'^(?=.*[a-z])'        # at least one lowercase
    r'(?=.*[A-Z])'         # at least one uppercase
    r'(?=.*\d)'            # at least one digit
    r'(?=.*[@$!%*?&])'     # at least one special char
    r'[A-Za-z\d@$!%*?&]{8,}$'  # allowed chars, min length 8
)

ONLY_ALPHANUMERIC_REGEX = r'^[a-zA-Z0-9]+$'  # only alphanumeric characters 