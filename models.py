from pydantic import BaseModel
from typing import Optional, List

class IngredientIn(BaseModel):
    name: str
    quantity: float
    unit: str
    notes: Optional[str] = None

class StepIn(BaseModel):
    order_num: int
    description: str

class RecipeCreate(BaseModel):
    name: str
    category_id: Optional[int] = None
    description: Optional[str] = None
    prep_time_min: Optional[int] = None
    servings: Optional[int] = None
    ingredients: List[IngredientIn] = []
    steps: List[StepIn] = []

class RecipeUpdate(RecipeCreate):
    pass