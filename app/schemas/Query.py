import strawberry
from app.models.Ingredient import IngredientList
from app.models.Models import MODELS
from app.schemas.Ingredient import Ingredient
from app.schemas.Recipe import Recipe
from typing import List, Annotated
from pydantic import Field
from app.externalModels.ninjaNutrients.Client import NinjaNutritionClient
from app.data.redis.config import CONFIG, EXPIRATION_TIME, STORE_NAME
from pydantic_redis import Store


@strawberry.type
class Query:
    @strawberry.field
    async def ingredients(
        self,
        foodQuery: Annotated[
            str,
            Field(
                description="Separate different food ingredients in a single query by commas"
            ),
        ],
    ) -> List[Ingredient]:
        # TODO change Redis OM package to https://github.com/redis/redis-om-python
        store = Store(
            name=STORE_NAME, redis_config=CONFIG, life_span_in_seconds=EXPIRATION_TIME
        )
        for model in MODELS:
            store.register_model(model)
        # store.i
        foodQuery = foodQuery.strip().lower()
        # Redis checks
        # ingredients = IngredientList.select(ids=[foodQuery])
        client = NinjaNutritionClient()
        foods = await client.query(foodQuery=foodQuery)
        ingredients: List[Ingredient] = [food.getIngredient() for food in foods]
        ingredientList = IngredientList(query=foodQuery, ingredients=ingredients)
        # Add to Redis
        IngredientList.insert(ingredientList)
        return ingredients

    @strawberry.field
    async def recipes(self) -> Recipe:
        return []
