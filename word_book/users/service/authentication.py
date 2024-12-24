from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from configs.database import get_db
from word_book.users.models import User

# Secret key for JWT
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create a CryptContext for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    # A JWT (JSON Web Token) is a compact, URL-safe means of
    # representing claims between two parties.
    # It consists of three parts:
    # Header: Specifies metadata, such as the signing algorithm.
    # Payload: Contains the claims (data).
    # Signature: Ensures the token's integrity and authenticity.

    # Payload represents the claims (payload) to be encoded into the JWT
    # SECRET_KEY is The secret key used to sign the token.
    # ALGORITHM Specifies the signing algorithm.

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def authenticate_user(username: str, password: str, db: Session):

    user = db.query(User).filter(User.username == username).one_or_none()

    if not user or not verify_password(password, user.password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(payload)
        print(username)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return {"username": username}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# Dependency to check if the user is an admin
def admin_required(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    print(user)
    user_object = (
        db.query(User)
        .filter(User.username == user["username"], User.role == "admin")
        .one_or_none()
    )
    if not user_object:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have admin access",
        )
    return user
