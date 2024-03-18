from pydantic import BaseModel, Field
from typing import Optional
import datetime
import enum

class MetadataModel(BaseModel):
    option_description: str = Field(default=None)
    date: datetime.date = Field(default=None)
    shop: str = Field(default=None)
    id: int = Field(default=None)

class FruitsModel(BaseModel):
    apple: int = Field(default=None, ge=0)
    pears: Optional[int] = Field(default=None, ge=0)

class VegetablesModel(BaseModel):
    carrots: Optional[int] = Field(default=None, ge=0)
    tomatoes: int = Field(default=None, ge=5)
    lattuce: Optional[int] = Field(default=None, ge=0)

class MeatModel(BaseModel):
    chicken : float = Field(default=None, ge=0)
    beef: Optional[float] = Field(default=None, le=5)
    pork: Optional[float] = Field(default=None, ge=0)

class DiaryModel(BaseModel):
    milk: int = Field(default=None, ge=2, le=5)
    cheese: Optional[int] = Field(default=None, ge=0)
    yogurt: int = Field(default=None, values=["normal", " fat"])