
from fastapi import APIRouter, HTTPException, status

# rotas de exportacao
importacao_router = APIRouter()


@importacao_router.get("/")
async def root():
    return {"message": "Hello importacao_router"}