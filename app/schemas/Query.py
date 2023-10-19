import strawberry
from app.schemas.Ingredient import Ingredient
from app.schemas.Recipe import Recipe
from typing import List, Annotated
from pydantic import Field
from app.externalModels.ninjaNutrients.Client import NinjaNutritionClient


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
        client = NinjaNutritionClient()
        foodQuery = foodQuery.strip()
        foods = await client.query(foodQuery=foodQuery)
        ingredients = [food.getIngredient() for food in foods]
        return ingredients

    @strawberry.field
    async def recipes(self) -> Recipe:
        return []
