from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float


from ..database import Base

class Product(Base):
    __tablename__ = "production"

    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String)
    product = Column(String)
    year = Column(Integer)
    production = Column(Float)