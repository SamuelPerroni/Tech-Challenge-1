
from fastapi import APIRouter, HTTPException, status

# rotas de exportacao
producao_router = APIRouter()


@producao_router.get("/")
async def root():
    return {"message": "Hello producao_router"}