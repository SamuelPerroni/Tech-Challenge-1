from pydantic import BaseModel
from datetime import date


class ExportacaoIn(BaseModel):
    year: int
    pais: str
    description_type: str
    quantity: int
    valor: float

class ExportacaoOut(ExportacaoIn):
    id: int

class ExportacaoUpdate(BaseModel):
    year: int | None = None
    pais: str | None = None
    description_type: str | None = None
    value: float | None = None
