from pydantic import BaseModel

class ImportIn(BaseModel):
    product: str
    year: int
    commerce: float
    description_type: str


class ImportOut(ImportIn):
    id: int
    pass


class ImportUpdate(ImportIn):
    pass