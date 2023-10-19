from pydantic import BaseModel, computed_field
from app.models import INGREDIENT_UNIT
from app.models.Ingredient import Ingredient
from typing import List, Tuple

# TODO add pydantic_redis Model instead of BaseModel to cache Recipes


class Macros(BaseModel):
    carbohydrates: Tuple[float, INGREDIENT_UNIT]
    fats: Tuple[float, INGREDIENT_UNIT]
    proteins: Tuple[float, INGREDIENT_UNIT]


class Recipe(BaseModel):
    name: str
    cuisine: str = "N/A"
    ingredients: List[Ingredient] = []
    description: str = ""

    @computed_field
    @property
    def macros(self) -> Macros:
        UNIT: INGREDIENT_UNIT = "g"
        CARBS: float = sum(
            [ingredient.carbohydrate.amount for ingredient in self.ingredients]
        )
        FATS: float = sum([ingredient.fat.amount for ingredient in self.ingredients])
        PROTEINS: float = sum(
            [ingredient.protein.amount for ingredient in self.ingredients]
        )
        MACROS = Macros(
            carbohydrates=(CARBS, UNIT), fats=(FATS, UNIT), proteins=(PROTEINS, UNIT)
        )
        return MACROS
