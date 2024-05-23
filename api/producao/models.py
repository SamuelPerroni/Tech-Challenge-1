from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select

from ..database import Base


class Producao(Base):

    __tablename__ = "producao"

    id = Column(Integer, primary_key=True , autoincrement=True)