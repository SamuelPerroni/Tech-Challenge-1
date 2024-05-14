from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select

from ..database import Base


class Processamento(Base):

    __tablename__ = "processamento"

    id = Column(Integer, primary_key=True , autoincrement=True)