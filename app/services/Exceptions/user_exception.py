from fastapi import HTTPException, status

from app.crud.user import check_password
def validate_user_login(existing_user, password):
    """Validate user login credentials."""
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if existing_user.auth_provider != "email":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please use the appropriate login method for your account."
        )
    if check_password(existing_user, password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not existing_user.is_active or not existing_user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please verify your email."
        )