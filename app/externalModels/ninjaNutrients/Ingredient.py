from pydantic import BaseModel
from typing import List
from app.models.Ingredient import Carbohydrate, Fat, Protein, Ingredient
from app.models import INGREDIENT_UNIT, INGREDIENT_CATEGORY


class Macros(BaseModel):
    fat: Fat
    carbs: Carbohydrate
    protein: Protein


class NinjaFood(BaseModel):
    name: str
    calories: float
    serving_size_g: float
    fat_total_g: float
    fat_saturated_g: float
    protein_g: float
    sodium_mg: float
    potassium_mg: float
    cholesterol_mg: float
    carbohydrates_total_g: float
    fiber_g: float
    sugar_g: float

    def getFat(self) -> Fat:
        fat = Fat(
            amount=self.fat_total_g,
            unit=INGREDIENT_UNIT.g.value,
        )
        return fat

    def getCarbs(self) -> Carbohydrate:
        carbs = Carbohydrate(
            amount=self.carbohydrates_total_g,
            unit=INGREDIENT_UNIT.g.value,
        )
        return carbs

    def getProtein(self) -> Protein:
        protein = Protein(
            amount=self.protein_g,
            unit=INGREDIENT_UNIT.g.value,
        )
        return protein

    def getMacros(self):
        macros = Macros(
            fat=self.getFat(), carbs=self.getCarbs(), protein=self.getProtein()
        )
        return macros

    def getIngredient(self) -> Ingredient:
        ingredient = Ingredient(
            name=self.name,
            calories=self.calories,
            unit=INGREDIENT_UNIT.g.value,
            servingSize=self.serving_size_g,
            carbohydrate=self.getCarbs(),
            fat=self.getFat(),
            protein=self.getProtein(),
        )
        return ingredient


class NinjaNutritionResult(BaseModel):
    query: str
    foods: List[NinjaFood]
