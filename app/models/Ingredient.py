from pydantic import Field
from app.models import INGREDIENT_UNIT, INGREDIENT_CATEGORY, ID_Factory
from pydantic_redis import Model
from typing import List


class Macro(Model):
    _primary_key_field: str = "id"
    id: str = Field(default_factory=ID_Factory)
    unit: str
    amount: float


class Carbohydrate(Macro):
    unit: str = INGREDIENT_UNIT.g.value


class Fat(Macro):
    unit: str = INGREDIENT_UNIT.g.value


class Protein(Macro):
    unit: str = INGREDIENT_UNIT.g.value


class Ingredient(Model):
    _primary_key_field: str = "name"
    name: str
    # TODO: figure out category
    # category: str
    calories: float
    unit: str
    servingSize: float
    carbohydrate: Carbohydrate
    fat: Fat
    protein: Protein


class IngredientList(Model):
    _primary_key_field: str = "query"
    query: str
    ingredients: List[Ingredient]


# Macro.model_rebuild()
# Carbohydrate.model_rebuild()
# Fat.model_rebuild()
# Protein.model_rebuild()
# Ingredient.model_rebuild()
# IngredientList.model_rebuild()
