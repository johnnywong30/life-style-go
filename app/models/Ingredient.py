from pydantic import Field, BaseModel
from app.models import INGREDIENT_UNIT, INGREDIENT_CATEGORY, ID_Factory
from typing import List


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
    name: str
    # TODO: figure out category
    # category: str
    calories: float
    unit: str
    servingSize: float
    carbohydrate: Carbohydrate
    fat: Fat
    protein: Protein


class IngredientList(BaseModel):
    query: str
    ingredients: List[Ingredient]
