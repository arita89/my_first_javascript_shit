from pydantic import BaseModel, Field
import datetime

class TemplateModel(BaseModel):
    option_description: str = Field(..., )
    date: datetime.date = Field(..., )
    shop: str = Field(..., )
    id: int = Field(..., )
    apple: int = Field(..., ge=0)
    pears: int = Field(..., ge=0)
    carrots: int = Field(..., ge=0)
    tomatoes: int = Field(..., ge=5)
    lattuce: int = Field(..., ge=0)
    chicken : float = Field(..., ge=0)
    beef: float = Field(..., le=5)
    pork: float = Field(..., ge=0)
    milk: int = Field(..., ge=2, le=5)
    cheese: int = Field(..., ge=0)
    yogurt: int = Field(..., values=["normal", " fat"])