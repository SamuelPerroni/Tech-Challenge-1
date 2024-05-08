
from fastapi import APIRouter, HTTPException, status

# rotas de exportacao
exportacao_router = APIRouter()


@exportacao_router.get("/")
async def root():
    return {"message": "Hello exportacao_router"}