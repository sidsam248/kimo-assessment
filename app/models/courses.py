from enum import Enum

from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List

from models.py_object_id import PyObjectId


class CoursesModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    date: int = Field(...)
    description: str = Field(...)
    domain: List[str] = Field(...)
    chapters: List[dict] = Field(...)
    ratings: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
