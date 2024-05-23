from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select

from ..database import Base


class Exportacao(Base):

    __tablename__ = "exportacao"

    id = Column(Integer, primary_key=True , autoincrement=True)