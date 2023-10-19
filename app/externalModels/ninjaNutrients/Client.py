from app.shared.helpers import AsyncClient
from typing import Dict, List
import os
import json
from dotenv import load_dotenv
from app.externalModels.ninjaNutrients.Ingredient import NinjaFood
from app.data.mongo.Food import addFoods, getFoods

load_dotenv()


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
        # TODO future for more efficiency; split the query by commas in order to
        # merge saved results and new results together
        foods = getFoods(query=foodQuery)
        if len(foods) == 0:
            # get new foods for query
            foods = await self.__queryNinja__(foodQuery)
            # insert into MongoDB
            foods = addFoods(query=foodQuery, foods=foods)
        return foods
