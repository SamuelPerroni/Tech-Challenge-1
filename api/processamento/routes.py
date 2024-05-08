
from fastapi import APIRouter, HTTPException, status

# rotas de exportacao
processamento_router = APIRouter()


@processamento_router.get("/")
async def root():
    return {"message": "Hello processamento_router"}