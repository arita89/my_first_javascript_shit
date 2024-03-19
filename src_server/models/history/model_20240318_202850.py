class DiaryModel(BaseModel):
    milk: int = Field(default=None, ge=2, le=5)
    cheese: Optional[int] = Field(default=None, ge=0)
    yogurt: int = Field(default=None, values=["normal", " fat"])