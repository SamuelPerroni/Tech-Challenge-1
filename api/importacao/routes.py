from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path, Query
from sqlalchemy.future import select

from .schemas import ImportIn, ImportOut, ImportUpdate
from .models import Importacao
from ..database import SessionLocal


# Import Routes - COMPLETE CRUD.
importacao_router = APIRouter()



# POST ENDPOINT.
@importacao_router.post("/", response_model=ImportOut, status_code=status.HTTP_201_CREATED)
async def create_Import(import_create: ImportIn):
    async with SessionLocal() as session:
        import_obj = await Importacao.get(session, **import_create.model_dump())
        if import_obj is None:
            import_to_create = Importacao(**import_create.model_dump())
            return await Importacao.create(session, import_to_create)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exists")


# GET ENDPOINT. LIST OF OBJECTS BY QUERY PARAMETERS
@importacao_router.get("/", response_model=list[ImportOut], status_code=status.HTTP_200_OK)
async def read_import(
    pais: Annotated[str | None, Query(description="Query for name of country")] = None,
    year: Annotated[int | None,  Query(description="Query data for specific year")] = None, 
    values: Annotated[int | None,  Query(description="Query data for specific values")] = None,
    quantity: Annotated[int | None,  Query(description="Query data for specific quantity")] = None,
    valor: Annotated[str | None,  Query(description="Query data for specific valor")] = None,
    type: Annotated[str | None, Query(description="Query for scpecific type of product")] = None):
    async with SessionLocal() as session:
        import_objs = await Importacao.get_all(
            session, 
            pais=pais, 
            year=year, 
            values=values, 
            quantity=quantity, 
            valor=valor, 
            type=type)
    return import_objs


# GET ENDPOINT. ONE OBJECT BY ID
@importacao_router.get("/{id}", response_model=ImportOut, status_code=status.HTTP_200_OK)
async def read_import_by_id(id: Annotated[int, Path(title="The ID of the item to get")]):
    async with SessionLocal() as session:
        query = select(Importacao).where(Importacao.id == id)
        result = await session.execute(query)
        import_objs = result.scalar()
        if import_objs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return import_objs


# UPDATE ENDPOINT
@importacao_router.put("/{id}", response_model=ImportOut, status_code=status.HTTP_200_OK)
async def update_import_object(id: Annotated[int, Path(title="The ID of the item to get")], Import_update: ImportUpdate):
    async with SessionLocal() as session:
        import_obj = await Importacao.get_by_id(session, id=id)
        if import_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        await Importacao.update(session, import_obj, **Import_update.model_dump())
    return import_obj


# DELETE ENDPOINT
@importacao_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_import_object(id: Annotated[int, Path(title="The ID of the item to get")]):
    async with SessionLocal() as session:
        import_obj = await Importacao.get_by_id(session, id=id)
        if import_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        await Importacao.delete(session, import_obj)
    return {"message": "deleted"} 

# # # # COMPLEX ENDPOINTS # # # #

# Get or Create implementation by outside function definitions.
@importacao_router.post("/get-or-create/", response_model=ImportOut, status_code=status.HTTP_201_CREATED)
async def get_or_create_import(import_create: ImportIn):
    async with SessionLocal() as session:
        obj = await Importacao.get_or_create(session, **import_create.model_dump())
    return obj


# Create or Update implementation by outise function definitions.
@importacao_router.post("/create-or-update/", response_model=ImportOut, status_code=status.HTTP_201_CREATED)
async def create_or_update_import(import_create: ImportIn):
    async with SessionLocal() as session:
        obj = await Importacao.create_or_update(session, **import_create.model_dump())
    return obj
