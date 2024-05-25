from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from .schemas import ProcessamentoIn, ProcessamentoOut, ProcessamentoUpdate
from .models import Processamento
from ..database import SessionLocal
from api.security.utils import auth_wrapper

# rotas de exportacao
processamento_router = APIRouter()


# POST ENDPOINT.
@processamento_router.post("/",
                           response_model=ProcessamentoOut,
                           status_code=status.HTTP_201_CREATED)
async def create_processamento(processamento_create: ProcessamentoIn,
                               username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        processamento_obj = await Processamento.get(session,**processamento_create.model_dump())
        if processamento_obj is None:
            processamento_to_create = Processamento(**processamento_create.model_dump())
            return await Processamento.create(session, processamento_to_create)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Object already exists")


# GET ENDPOINT. ONE OBJECT BY ID
@processamento_router.get("/{id}",
                          response_model=ProcessamentoOut,
                          status_code=status.HTTP_200_OK)
async def read_processamento_by_id(id: Annotated[int,
                                                 Path(title="The ID of the item to get")]):

    async with SessionLocal() as session:
        processamento_objs = await Processamento.get_by_id(session, id)
        if processamento_objs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Object not found")
    return processamento_objs


# GET ENDPOINT. LIST OF OBJECTS BY QUERY PARAMETERS
@processamento_router.get("/",
                          response_model=list[ProcessamentoOut],
                          status_code=status.HTTP_200_OK)
async def read_processamento(
    product_type: Annotated[str | None,
                            Query(description="Query data for specific type of product")] = None,
    full_product_name: Annotated[str | None,
                                 Query(description="Query for scpecific product")] = None,
    classification: Annotated[str | None,
                              Query(description="Query data for specific classification.")] = None,
    year: Annotated[int | None,
                    Query(description="Query data for specific year")] = None):

    async with SessionLocal() as session:
        processamento_objs = await Processamento.get_all(session,
                                                         product_type=product_type,
                                                         full_product_name=full_product_name,
                                                         classification=classification,
                                                         year=year)
    return processamento_objs


# UPDATE ENDPOINT
@processamento_router.put("/{id}",
                          response_model=ProcessamentoOut,
                          status_code=status.HTTP_200_OK)
async def update_comercio_object(id: Annotated[int, Path(title="The ID of the item to get")],
                                 processamento_update: ProcessamentoUpdate,
                                 username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        processamento_obj = await Processamento.get_by_id(session,
                                                          id=id)
        if processamento_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Object not found")
        await Processamento.update(session, processamento_obj,
                                   **processamento_update.model_dump())
    return processamento_obj


# DELETE ENDPOINT
@processamento_router.delete('/{id}',
                             status_code=status.HTTP_200_OK)
async def delete_processamento_object(id: Annotated[int, Path(title="The ID of the item to get")],
                                      username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        processamento_obj = await Processamento.get_by_id(session, id=id)
        if processamento_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Object not found")
        await Processamento.delete(session,
                                   processamento_obj)
    return {"message": "deleted"}

# # # # COMPLEX ENDPOINTS # # # #


# Get or Create implementation by outside function definitions.
@processamento_router.post("/get-or-create/",
                           response_model=ProcessamentoOut,
                           status_code=status.HTTP_201_CREATED)
async def get_or_create_processamento(processamento_create: ProcessamentoIn,
                                      username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        obj = await Processamento.get_or_create(session, **processamento_create.model_dump())
    return obj


# Create or Update implementation by outise function definitions.
@processamento_router.post("/create-or-update/",
                           response_model=ProcessamentoOut,
                           status_code=status.HTTP_201_CREATED)
async def create_or_update_processamento(processamento_create: ProcessamentoIn,
                                         username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        obj = await Processamento.create_or_update(session,
                                                   **processamento_create.model_dump())
    return obj
