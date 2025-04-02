from typing import Optional
from pydantic import BaseModel


class MuscleGroup(BaseModel):
    id:   int
    name: str


class CreateMuscleGroup(BaseModel):
    name: str


class UpdateMuscleGroup(BaseModel):
    name: str


class ReturnMuscleGroups(BaseModel):
    data:  list[MuscleGroup]
    total: int
    limit: int
    page:  int


class ReturnMuscleGroup(BaseModel):
    data:    Optional[MuscleGroup] = None
    message: Optional[str] = None


class ReturnMuscleGroupId(BaseModel):
    id:      Optional[int] = None
    message: Optional[str] = None
