from pydantic import BaseModel


class ProcessamentoIn(BaseModel):
    product_type: str
    full_product_name: str
    classification: str
    year: int
    commerce: float


class ProcessamentoOut(ProcessamentoIn):
    id: int
    pass


class ProcessamentoUpdate(BaseModel):
    product_type: str | None = None
    full_product_name: str | None = None
    classification: str | None = None
    year: int | None = None
    commerce: float | None = None
