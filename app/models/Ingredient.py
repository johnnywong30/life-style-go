from pydantic import BaseModel, Field
from app.models import INGREDIENT_UNIT, INGREDIENT_CATEGORY, ID_Factory
from typing import List, Dict


class Macro(BaseModel):
    unit: str
    amount: float


class Carbohydrate(Macro):
    unit: str = INGREDIENT_UNIT.g.value


class Fat(Macro):
    unit: str = INGREDIENT_UNIT.g.value


class Protein(Macro):
    unit: str = INGREDIENT_UNIT.g.value


class Ingredient(BaseModel):
    id: str = Field(default_factory=ID_Factory)
    name: str
    calories: float
    unit: str
    servingSize: float
    carbohydrate: Carbohydrate
    fat: Fat
    protein: Protein


class IngredientList(BaseModel):
    query: str
    ingredients: List[Ingredient]
