from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float, and_
from sqlalchemy.future import select

from ..database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(32))
    user_pass = Column(String(123))

    def __repr__(self):
        return f"{self.user_name}"

    @classmethod
    async def get(cls, session, user_name):
        busca = await session.scalar(select(cls).where(
            cls.user_name == user_name))
        return busca

    @classmethod
    async def create(cls, session, obj_to_create):
        session.add(obj_to_create)
        await session.commit()
        return obj_to_create

    @classmethod
    async def update(cls, session, obj_to_update, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                setattr(obj_to_update, field, value)
        await session.commit()
        return obj_to_update

    @classmethod
    async def delete(cls, session, obj_to_delete):
        await session.delete(obj_to_delete)
        await session.commit()
