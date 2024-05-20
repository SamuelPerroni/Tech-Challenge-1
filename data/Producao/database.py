package_name = 'database'

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:changeme@localhost/dbml1"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20, pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "production"

    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String)
    product = Column(String)
    year = Column(Integer)
    production = Column(Float)

