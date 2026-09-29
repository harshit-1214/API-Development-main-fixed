import logging
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_async_db
from app.model import User
from app.schema import TokenData

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug("access token issued user_id=%s expires_at=%s", data.get("user_id"), expire)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            logger.warning("token rejected: missing user_id claim")
            raise credentials_exceptions
        token_data = TokenData(id=user_id)
    except JWTError as exc:
        logger.warning("token rejected: %s", exc)
        raise credentials_exceptions
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid id not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exceptions)

    user = await db.get(User, token.id)
    if user is None:
        logger.warning("token valid but user_id=%s no longer exists", token.id)
        raise credentials_exceptions
    return user