from pydantic import BaseModel


class ExportacaoIn(BaseModel):
    year: int
    pais: str
    type: str
    quantity: int
    valor: float

class ExportacaoOut(ExportacaoIn):
    id: int

class ExportacaoUpdate(BaseModel):
    year: int | None = None
    pais: str | None = None
    type: str | None = None
    valor: float | None = None
    quantity: int | None = None
