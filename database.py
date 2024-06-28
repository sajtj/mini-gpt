from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./sqlite.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = async_sessionmaker(engine)

class Base(DeclarativeBase) :
    pass

async def get_db() :
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try :
        yield db
    finally :
        await db.close()