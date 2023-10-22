import strawberry
from app.models.Ingredient import IngredientList
from app.schemas.Ingredient import Ingredient
from app.schemas.Recipe import Recipe
from typing import List, Annotated
from pydantic import Field
from app.externalModels.ninjaNutrients.Client import NinjaNutritionClient
from app.data.redis.connection import getRedisConnection


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
        foodQuery = foodQuery.strip().lower()
        ingredients: List[Ingredient]
        with getRedisConnection() as RedisClient:
            # Redis checks
            ingredientList: IngredientList | None
            ingredientList = RedisClient.getIngredients(foodQuery)
            if not ingredientList:
                client = NinjaNutritionClient()
                foods = await client.query(foodQuery=foodQuery)
                ingredients = [food.getIngredient() for food in foods]
                ingredientList = IngredientList(
                    query=foodQuery, ingredients=ingredients
                )
                # Add to Redis
                RedisClient.setIngredients(foodQuery, ingredientList)
            else:
                ingredients = ingredientList.ingredients
        return ingredients

    @strawberry.field
    async def recipes(self) -> List[Recipe]:
        return []
