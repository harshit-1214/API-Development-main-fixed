import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.model import User as user_table
from app.oauth2 import create_access_token
from app.utils import verify_password

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/login", tags=["Auth"])


@router.post("/")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(user_table).where(user_table.email == user_credentials.username))
    user = result.scalar_one_or_none()
    if not user:
        logger.warning("login failed: unknown email %s", user_credentials.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    password_ok = await run_in_threadpool(verify_password, user_credentials.password, user.password)
    if not password_ok:
        logger.warning("login failed: wrong password user_id=%s", user.id)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})
    logger.info("login success user_id=%s", user.id)
    return {"access_token": access_token, "token_type": "bearer"}