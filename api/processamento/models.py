from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.future import select

from ..database import Base


class Processamento(Base):

    __tablename__ = "processamento"

    id = Column(Integer, primary_key=True , autoincrement=True)
    product_type = Column(String(32))
    full_product_name = Column(String(32))
    classification = Column(String(32))
    year = Column(Integer)
    commerce = Column(Float)

    def __repr__(self):
        return f"{self.product_type} - {self.full_product_name} - {self.classification} - {self.year} - {self.commerce}"
    
    @classmethod
    async def get(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('product_type') is not None:
            query = query.where(cls.product_type == kwargs.get('product_type'))
        if kwargs.get('full_product_name') is not None:
            query = query.where(cls.full_product_name == kwargs.get('full_product_name'))
        if kwargs.get('classification') is not None:
            query = query.where(cls.classification == kwargs.get('classification'))
        if kwargs.get('year') is not None:
            query = query.where(cls.year == kwargs.get('year'))
        #result = await session.execute(query)
        return await session.scalar(query)
    
    @classmethod
    async def get_all(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('product_type') is not None:
            query = query.where(cls.product_type == kwargs.get('product_type'))
        if kwargs.get('full_product_name') is not None:
            query = query.where(cls.full_product_name == kwargs.get('full_product_name'))
        if kwargs.get('classification') is not None:
            query = query.where(cls.classification == kwargs.get('classification'))
        if kwargs.get('year') is not None:
            query = query.where(cls.year == kwargs.get('year'))
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    async def get_by_id(cls, session, id):
        query = select(cls).where(cls.id == id)
        #result = await session.execute(query)
        return await session.scalar(query)
  
    @classmethod
    async def create(cls, session, obj_to_create):
        session.add(obj_to_create)
        await session.commit()
        return obj_to_create
    
    @classmethod
    async def update(cls, session, old_obj, **new_obj):
        for field, value in new_obj.items():
            if value != None:
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
