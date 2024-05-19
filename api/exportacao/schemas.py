from pydantic import BaseModel
from datetime import date


class ExportacaoIn(BaseModel):
    year: int
    pais: str
    description_type: str
    value: float


class ExportacaoOut(ExportacaoIn):
    id: int

    class Config:
        orm_mode = True


class ExportacaoUpdate(BaseModel):
    year: int | None = None
    pais: str | None = None
    description_type: str | None = None
    value: float | None = None
