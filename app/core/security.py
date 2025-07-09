from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 3. Function to verify a plain password against a hashed one
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
