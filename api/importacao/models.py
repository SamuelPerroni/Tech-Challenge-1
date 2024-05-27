from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select

from ..database import Base


class Importacao(Base):

    __tablename__ = "importacao"

    id = Column(Integer, primary_key=True , autoincrement=True)
    pais = Column(String(60))
    year = Column(Integer)
    quantity = Column(Integer)
    valor = Column(Integer)
    type = Column(String(60))

    def __repr__(self):
        return f"{self.pais} - {self.year} - {self.quantity} - {self.valor} - {self.type}"

    @classmethod
    async def get(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('pais') is not None:
            query = query.where(cls.pais == kwargs.get('pais'))
        if kwargs.get('year') is not None:
            query = query.where(cls.year == kwargs.get('year'))
        if kwargs.get('type') is not None:
            query = query.where(cls.type == kwargs.get('type'))
        result = await session.execute(query)
        return result.scalar()
    
    @classmethod
    async def get_all(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('pais') is not None:
            query = query.where(cls.pais == kwargs.get('pais'))
        if kwargs.get('year') is not None:
            query = query.where(cls.year == kwargs.get('year'))
        if kwargs.get('quantity') is not None:
            query = query.where(cls.quantity == kwargs.get('quantity'))
        if kwargs.get('valor') is not None:
            query = query.where(cls.valor == kwargs.get('valor'))
        if kwargs.get('type') is not None:
            query = query.where(cls.type == kwargs.get('type'))
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
