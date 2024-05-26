from pydantic import BaseModel

class ImportIn(BaseModel):
    pais: str
    year: int
    values: float
    quantity: float
    valor: float
    type: str


class ImportOut(ImportIn):
    id: int
    pass


class ImportUpdate(ImportIn):
    pass
