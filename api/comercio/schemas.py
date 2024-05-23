from pydantic import BaseModel

class ComercioIn(BaseModel):
    product: str
    year: int
    commerce: float
    description_type: str


class ComercioOut(ComercioIn):
    id: int
    pass


class ComercioUpdate(ComercioIn):
    pass