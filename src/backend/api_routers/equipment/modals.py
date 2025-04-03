from typing import Optional
from pydantic import BaseModel


class Equipment(BaseModel):
    id:          int
    name:        str
    description: Optional[str] = None


class CreateEquipment(BaseModel):
    name:        str
    description: Optional[str] = None

class UpdateEquipment(BaseModel):
    name:        str
    description: Optional[str] = None


class ReturnEquipmentAll(BaseModel):
    data:  list[Equipment]
    total: int
    limit: int
    page:  int


class ReturnEquipment(BaseModel):
    data:    Optional[Equipment] = None
    message: Optional[str] = None


class ReturnEquipmentId(BaseModel):
    id:      Optional[int] = None
    message: Optional[str] = None
