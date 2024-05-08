from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path, Query
from sqlalchemy.future import select

from .schemas import ComercioIn, ComercioOut, ComercioUpdate, ComercioDelete
from .models import Comercio
from ..database import SessionLocal


# Comercio Routes - COMPLETE CRUD.
comercio_router = APIRouter()



# POST ENDPOINT.
@comercio_router.post("/", response_model=ComercioOut, status_code=status.HTTP_201_CREATED)
async def create_comercio(comercio_create: ComercioIn):
    async with SessionLocal() as session:
        comercio_obj = await Comercio.get(session, **comercio_create.model_dump())
        if comercio_obj is None:
            comercio_to_create = Comercio(**comercio_create.model_dump())
            session.add(comercio_to_create)
            await session.commit()
            return comercio_to_create
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exists")


# GET ENDPOINT. LIST OF OBJECTS BY QUERY PARAMETERS
@comercio_router.get("/", response_model=list[ComercioOut], status_code=status.HTTP_200_OK)
async def read_comercio(
    year: Annotated[int | None,  Query(description="Query data for specific year")] = None, 
    product: Annotated[str | None,  Query(description="Query data for specific product")] = None,  
    description_type: Annotated[str | None, Query(description="Query for scpecific type of product")] = None):
    async with SessionLocal() as session:
        query = select(Comercio)
        if year is not None:
            query = query.where(Comercio.year == year)
        if product is not None:
            query = query.where(Comercio.product == product)
        if description_type is not None:
            query = query.where(Comercio.description_type == description_type)     
        result = await session.execute(query)
        comercio_objs = result.scalars().all()
    
    return comercio_objs


# GET ENDPOINT. ONE OBJECT BY ID
@comercio_router.get("/{id}", response_model=ComercioOut, status_code=status.HTTP_200_OK)
async def read_comercio_by_id(id: Annotated[int, Path(title="The ID of the item to get")]):
    async with SessionLocal() as session:
        query = select(Comercio).where(Comercio.id == id)
        result = await session.execute(query)
        comercio_objs = result.scalar()
        if comercio_objs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return comercio_objs


# UPDATE ENDPOINT
@comercio_router.put("/{id}", response_model=ComercioOut, status_code=status.HTTP_200_OK)
async def update_comercio_object(id: Annotated[int, Path(title="The ID of the item to get")], comercio_update: ComercioUpdate):
    async with SessionLocal() as session:
        # Check if object exists
        query = select(Comercio).where(Comercio.id == id)
        result = await session.execute(query)
        comercio_obj = result.scalar()
        if comercio_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        for field, value in comercio_update.model_dump(exclude_unset=True).items():
            setattr(comercio_obj, field, value)
        await session.commit()
    return comercio_obj


# DELETE ENDPOINT
@comercio_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_comercio_object(id: Annotated[int, Path(title="The ID of the item to get")]):
    async with SessionLocal() as session:
        # Check if object exists
        query = select(Comercio).where(Comercio.id == id)
        result = await session.execute(query)
        comercio_obj = result.scalar()
        if comercio_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        await session.delete(comercio_obj)
        await session.commit()

    return {"message": "deleted"} 

# # # # COMPLEX ENDPOINTS # # # #

# Get or Create implementation by outside function definitions.
@comercio_router.post("/get-or-create/", response_model=ComercioOut, status_code=status.HTTP_201_CREATED)
async def get_or_create_comercio(comercio_create: ComercioIn):
    async with SessionLocal() as session:
        obj = await Comercio.get_or_create(session, **comercio_create.model_dump())
    return obj


# Create or Update implementation by outise function definitions.
@comercio_router.post("/create-or-update/", response_model=ComercioOut, status_code=status.HTTP_201_CREATED)
async def create_or_update_comercio(comercio_create: ComercioIn):
    async with SessionLocal() as session:
        obj = await Comercio.create_or_update(session, **comercio_create.model_dump())
    return obj
