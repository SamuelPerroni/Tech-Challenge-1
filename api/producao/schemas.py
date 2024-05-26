from pydantic import BaseModel


class ProducaoIn(BaseModel):
    type: str
    full_product_name: str
    year: int
    value: float


class ProducaoOut(ProducaoIn):
    id: int
    pass


class ProducaoUpdate(BaseModel):
    type: str | None = None
    full_product_name: str | None = None
    year: int | None = None
    value: float | None = None