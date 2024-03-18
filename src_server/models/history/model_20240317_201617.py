from pydantic import BaseModel, Field
from typing import Optional
import datetime

class TemplateModel(BaseModel):
    option_description: str = Field(..., )
    date: datetime.date = Field(..., )
    shop: str = Field(..., )
    id: int = Field(..., )
    apple: int = Field(..., ge=0)
    pears: Optional[int] = Field(None, ge=0)
    carrots: Optional[int] = Field(None, ge=0)
    tomatoes: int = Field(..., ge=5)
    lattuce: Optional[int] = Field(None, ge=0)
    chicken : float = Field(..., ge=0)
    beef: Optional[float] = Field(None, le=5)
    pork: Optional[float] = Field(None, ge=0)
    milk: int = Field(..., ge=2, le=5)
    cheese: Optional[int] = Field(None, ge=0)
    yogurt: int = Field(..., values=["normal", " fat"])