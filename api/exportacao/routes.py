from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.future import select

from .schemas import ExportacaoIn, ExportacaoOut, ExportacaoUpdate
from .models import Exportacao
from ..database import SessionLocal
from api.security.utils import auth_wrapper


# ExportacaoRoutes - COMPLETE CRUD.
exportacao_router = APIRouter()


@exportacao_router.post("/", response_model=ExportacaoOut, status_code=status.HTTP_201_CREATED)
async def create_exportacao(create_exportacao: ExportacaoIn, username=Depends(auth_wrapper)):
    async with SessionLocal() as session:
        exportacao_obj = await Exportacao.get(session, **create_exportacao.model_dump())
        if exportacao_obj is None:
            create_exportacao = Exportacao(**create_exportacao.model_dump())
            return await Exportacao.create(session, create_exportacao)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exists")


# GET ENDPOINT. LIST OF OBJECTS BY QUERY PARAMETERS
@exportacao_router.get("/", response_model=list[ExportacaoOut], status_code=status.HTTP_200_OK)
async def read_exportacao(
    year: Annotated[int | None, Query(description="Query data for specific year")] = None,
    pais: Annotated[str | None, Query(description="Query data for specific product")] = None,
    type: Annotated[str | None, Query(description="Query for specific type of product")] = None):
    async with SessionLocal() as session:
        exportacao_objs = await Exportacao.get_all(session, year=year, pais=pais, type=type)
    return exportacao_objs


# GET ENDPOINT. ONE OBJECT BY ID
@exportacao_router.get("/{id}", response_model=ExportacaoOut, status_code=status.HTTP_200_OK)
async def read_exportacao_by_id(id: Annotated[int, Path(title="The ID of the item to get")]):
    async with SessionLocal() as session:
        query = select(Exportacao).where(Exportacao.id == id)
        result = await session.execute(query)
        exportacao_objs = result.scalar()
        if exportacao_objs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return exportacao_objs


# UPDATE ENDPOINT
@exportacao_router.put("/{id}", response_model=ExportacaoOut, status_code=status.HTTP_200_OK)
async def update_exportacao_object(id: Annotated[int, Path(title="The ID of the item to get")], 
                                   exportacao_update: ExportacaoUpdate, 
                                   username=Depends(auth_wrapper)):
    async with SessionLocal() as session:
        exportacao_obj = await Exportacao.get_by_id(session, id=id)
        if exportacao_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        await Exportacao.update(session, exportacao_obj, **exportacao_update.model_dump())
    return exportacao_obj


# DELETE ENDPOINT
@exportacao_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_exportacao_object(id: Annotated[int, Path(title="The ID of the item to get")],
                                   username=Depends(auth_wrapper)):
    async with SessionLocal() as session:
        exportacao_obj = await Exportacao.get_by_id(session, id=id)
        if exportacao_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        await Exportacao.delete(session, exportacao_obj)
    return {"message": "deleted"}

# # # # COMPLEX ENDPOINTS # # # #

# Get or Create implementation by outside function definitions.
@exportacao_router.post("/get-or-create/", response_model=ExportacaoOut, status_code=status.HTTP_201_CREATED)
async def get_or_create_exportacao(exportacao_create: ExportacaoIn,
                                   username=Depends(auth_wrapper)):
    async with SessionLocal() as session:
        obj = await Exportacao.get_or_create(session, **exportacao_create.model_dump())
    return obj


# Create or Update implementation by outise function definitions.
@exportacao_router.post("/create-or-update/", response_model=ExportacaoOut, status_code=status.HTTP_201_CREATED)
async def create_or_update_exportacao(exportacao_create: ExportacaoIn,
                                      username=Depends(auth_wrapper)):
    async with SessionLocal() as session:
        obj = await Exportacao.create_or_update(session, **exportacao_create.model_dump())
    return obj
