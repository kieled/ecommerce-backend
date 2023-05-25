from typing import TypedDict

from pydantic import BaseModel


class MaterialsType(TypedDict):
    name: str
    value: str


class DescriptionSchema(BaseModel):
    id: int
    title: str
    description: str
    price: int
    materials: list[MaterialsType]
    sizes: list[str]
