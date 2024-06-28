from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from database import get_db
from models import User, Query
from schemas import UserBase


SECRET_KEY = "09d9f1d6a40b4b8eb7e49985f431bbbe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def create_user(db: AsyncSession, user: UserBase):
    db_user = User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username==username))
    user = result.scalars().first()
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: AsyncSession, username: str):
    user = get_user(db, username)
    if not user:
        return False
    return user

async def get_current_user( db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = await get_user(db, username=username)

    except JWTError:
        raise credentials_exception

    return user


async def create_query(db: AsyncSession, prompt: str, response: str, tokens: int, llm_name: str, user_id: int):
    db_query = Query(
        prompt=prompt,
        response=response,
        tokens=tokens,
        llm_name=llm_name,
        user_id=user_id
    )
    db.add(db_query)
    await db.commit()
    await db.refresh(db_query)
    return db_query


async def get_queries(db: AsyncSession, user_id: int):
    result = await db.execute(select(Query).where(Query.user_id == user_id).order_by(desc(Query.id)))
    queries = result.scalars().all() 
    return queries