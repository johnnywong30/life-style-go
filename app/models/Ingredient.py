from pydantic import BaseModel
from app.models import INGREDIENT_UNIT
from typing import Literal

MACRO_NAME = Literal["Carbohydrate", "Fat", "Protein"]
INGREDIENT_CATEGORY = Literal["Meat", "Vegetable", "Fruit", "Carbohydrate"]


class Macro(BaseModel):
    unit: INGREDIENT_UNIT
    amount: float


class Carbohydrate(Macro):
    unit: INGREDIENT_UNIT = "g"


class Fat(Macro):
    unit: INGREDIENT_UNIT = "g"


class Protein(Macro):
    unit: INGREDIENT_UNIT = "g"


class Ingredient(BaseModel):
    name: str
    # category: INGREDIENT_CATEGORY
    calories: float
    unit: INGREDIENT_UNIT
    servingSize: float
    carbohydrate: Carbohydrate
    fat: Fat
    protein: Protein
