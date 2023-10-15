from app.shared.helpers import AsyncClient
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict, List
from app.models.Ingredient import Carbohydrate, Fat, Protein, Ingredient
from app.data.mongo.Food import getFoods, addFoods

load_dotenv()


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
        fat = Fat(amount=self.fat_total_g)
        return fat

    def getCarbs(self) -> Carbohydrate:
        carbs = Carbohydrate(amount=self.carbohydrates_total_g)
        return carbs

    def getProtein(self) -> Protein:
        protein = Protein(amount=self.protein_g)
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
            unit="g",
            servingSize=self.serving_size_g,
            carbohydrate=self.getCarbs(),
            fat=self.getFat(),
            protein=self.getProtein(),
        )
        return ingredient


class NinjaNutritionResult(BaseModel):
    query: str
    foods: List[NinjaFood]


class NinjaNutritionClient:
    client: AsyncClient
    api_key: str
    ninja_url: str
    headers: Dict[str, str]

    def __init__(self):
        self.client = AsyncClient()
        self.api_key = os.getenv("NINJA_API_KEY")
        self.ninja_url = "https://api.api-ninjas.com/v1/nutrition"
        self.headers = {"X-Api-Key": self.api_key}

    async def __queryNinja__(self, foodQuery: str) -> List[NinjaFood]:
        queryURL = f"{self.ninja_url}?query={foodQuery}"
        response = await self.client.get(url=queryURL, headers=self.headers)
        ninjaFoods: List[Dict[str, str]] = json.loads(response.text)
        ninjaFoods = [NinjaFood(**food) for food in ninjaFoods]
        return ninjaFoods

    async def query(self, foodQuery: str) -> List[NinjaFood]:
        foodQuery = foodQuery.strip().lower()
        foods = getFoods(query=foodQuery)
        if len(foods) == 0:
            # get new foods for query
            foods = await self.__queryNinja__(foodQuery)
            # insert into MongoDB
            foods = addFoods(query=foodQuery, foods=foods)
        return foods
