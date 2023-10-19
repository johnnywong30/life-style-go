from typing import List
from pydantic_redis import Model
from app.models.Ingredient import (
    Macro,
    Carbohydrate,
    Fat,
    Protein,
    Ingredient,
    IngredientList,
)

# TODO: import Recipe models when ready for Redis
# from app.models.Recipe


MODELS: List[Model] = [
    Macro,
    Carbohydrate,
    Fat,
    Protein,
    Ingredient,
    IngredientList,
]
