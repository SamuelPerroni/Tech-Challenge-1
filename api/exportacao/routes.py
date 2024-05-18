
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Path, Query
from sqlalchemy.future import select
from .schemas import ComercioIn, ComercioOut, ComercioUpdate
from .models import Comercio
from ..database import SessionLocal

# rotas de exportacao
exportacao_router = APIRouter()


@exportacao_router.get("/")
async def root():
    return {"message": "Hello exportacao_router"}