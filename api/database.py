from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlite3

from .config import settings

engine = create_async_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    future=True,
    class_=AsyncSession 
    )

Base = declarative_base()
