from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from .schemas import ProducaoIn, ProducaoOut, ProducaoUpdate
from .models import Producao
from ..database import SessionLocal
from api.security.utils import auth_wrapper

# rotas de exportacao
producao_router = APIRouter()


# POST ENDPOINT.
@producao_router.post("/",
                           response_model=ProducaoOut,
                           status_code=status.HTTP_201_CREATED)
async def create_Producao(Producao_create: ProducaoIn,
                               username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        Producao_obj = await Producao.get(session,**Producao_create.model_dump())
        if Producao_obj is None:
            Producao_to_create = Producao(**Producao_create.model_dump())
            return await Producao.create(session, Producao_to_create)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Object already exists")


# GET ENDPOINT. ONE OBJECT BY ID
@producao_router.get("/{id}",
                          response_model=ProducaoOut,
                          status_code=status.HTTP_200_OK)
async def read_Producao_by_id(id: Annotated[int,
                                                 Path(title="The ID of the item to get")]):

    async with SessionLocal() as session:
        Producao_objs = await Producao.get_by_id(session, id)
        if Producao_objs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Object not found")
    return Producao_objs


# GET ENDPOINT. LIST OF OBJECTS BY QUERY PARAMETERS
@producao_router.get("/",
                          response_model=list[ProducaoOut],
                          status_code=status.HTTP_200_OK)
async def read_Producao(
    type: Annotated[str | None,
                            Query(description="Query data for specific type of product")] = None,
    full_product_name: Annotated[str | None,
                                 Query(description="Query for scpecific product")] = None,
    year: Annotated[int | None,
                    Query(description="Query data for specific year")] = None):

    async with SessionLocal() as session:
        Producao_objs = await Producao.get_all(session,
                                                         type=type,
                                                         full_product_name=full_product_name,
                                                         year=year)
    return Producao_objs


# UPDATE ENDPOINT
@producao_router.put("/{id}",
                          response_model=ProducaoOut,
                          status_code=status.HTTP_200_OK)
async def update_comercio_object(id: Annotated[int, Path(title="The ID of the item to get")],
                                 Producao_update: ProducaoUpdate,
                                 username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        Producao_obj = await Producao.get_by_id(session,
                                                          id=id)
        if Producao_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Object not found")
        await Producao.update(session, Producao_obj,
                                   **Producao_update.model_dump())
    return Producao_obj


# DELETE ENDPOINT
@producao_router.delete('/{id}',
                             status_code=status.HTTP_200_OK)
async def delete_Producao_object(id: Annotated[int, Path(title="The ID of the item to get")],
                                      username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        Producao_obj = await Producao.get_by_id(session, id=id)
        if Producao_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Object not found")
        await Producao.delete(session,
                                   Producao_obj)
    return {"message": "deleted"}

# # # # COMPLEX ENDPOINTS # # # #


# Get or Create implementation by outside function definitions.
@producao_router.post("/get-or-create/",
                           response_model=ProducaoOut,
                           status_code=status.HTTP_201_CREATED)
async def get_or_create_Producao(Producao_create: ProducaoIn,
                                      username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        obj = await Producao.get_or_create(session, **Producao_create.model_dump())
    return obj


# Create or Update implementation by outise function definitions.
@producao_router.post("/create-or-update/",
                           response_model=ProducaoOut,
                           status_code=status.HTTP_201_CREATED)
async def create_or_update_Producao(Producao_create: ProducaoIn,
                                         username=Depends(auth_wrapper)):

    async with SessionLocal() as session:
        obj = await Producao.create_or_update(session,
                                                   **Producao_create.model_dump())
    return obj
