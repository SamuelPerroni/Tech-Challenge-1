from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select

from ..database import Base


class Comercio(Base):

    __tablename__ = "comercio"

    id = Column(Integer, primary_key=True , autoincrement=True)
    product = Column(String(60))
    year = Column(Integer)
    description_type = Column(String(60))
    commerce = Column(Float)

    def __repr__(self):
        return f"{self.product} - {self.year} - {self.description_type} - {self.commerce}"

    @classmethod
    async def get(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('year') is not None:
            query = query.where(cls.year == kwargs.get('year'))
        if kwargs.get('product') is not None:
            query = query.where(cls.product == kwargs.get('product'))
        if kwargs.get('description_type') is not None:
            query = query.where(cls.description_type == kwargs.get('description_type'))
        result = await session.execute(query)
        return result.scalar()
    
    @classmethod
    async def get_all(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('year') is not None:
            query = query.where(cls.year == kwargs.get('year'))
        if kwargs.get('product') is not None:
            query = query.where(cls.product == kwargs.get('product'))
        if kwargs.get('description_type') is not None:
            query = query.where(cls.description_type == kwargs.get('description_type'))
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    async def get_by_id(cls, session, id):
        query = select(cls).where(cls.id == id)
        result = await session.execute(query)
        comercio_obj = result.scalar()
        return comercio_obj
    
    @classmethod
    async def create(cls, session, obj_to_create):
        session.add(obj_to_create)
        await session.commit()
        return obj_to_create
    
    @classmethod
    async def update(cls, session, old_obj, **new_obj):
        for field, value in new_obj.items():
            setattr(old_obj, field, value)
        await session.commit()
        return old_obj

    @classmethod
    async def delete(cls, session, obj_to_delete):
        await session.delete(obj_to_delete)
        await session.commit()

    @classmethod
    async def get_or_create(cls, session, **kwargs):
        obj = await cls.get(session,  **kwargs)
        if obj is None:
            obj_to_create = cls(**kwargs)
            return await cls.create(session,  obj_to_create)
        return obj
    
    @classmethod
    async def create_or_update(cls, session, **kwargs):
        obj = await cls.get(session,  **kwargs)
        if obj is None:
            obj_to_create = cls(**kwargs)
            return await cls.create(session, obj_to_create)
        return await cls.update(session, obj, **kwargs)
