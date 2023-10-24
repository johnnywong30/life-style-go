import strawberry
from app.models.Recipe import Recipe as PydanticRecipe, Patch_Recipe
from app.models.Ingredient import Ingredient as PydanticIngredient
from app.schemas.Recipe import Recipe
from app.schemas.Ingredient import (
    Ingredient,
    BaseIngredient,
    Fat,
    Protein,
    Carbohydrate,
)
from app.data.mongo.Recipes import (
    getRecipe,
    addRecipe,
    delRecipe,
    updateRecipe,
    addIngredients,
    delIngredients,
    updateIngredients,
)
from typing import List
from app.externalModels.ninjaNutrients.Client import NinjaNutritionClient
from app.externalModels.ninjaNutrients.Ingredient import NinjaFood


async def queryIngredients(
    baseIngredients: List[BaseIngredient],
) -> List[PydanticIngredient]:
    nutritionClient = NinjaNutritionClient()
    ninjaFoods: List[NinjaFood] = [
        food
        for foodList in [
            await nutritionClient.query(ingredient.name)
            for ingredient in baseIngredients
        ]
        for food in foodList
    ]
    queriedIngredients: List[PydanticIngredient] = [
        food.getIngredient() for food in ninjaFoods
    ]
    return queriedIngredients


def generateRecipeGraphQL(recipe: PydanticRecipe) -> Recipe:
    recipe = Recipe(
        id=recipe.id,
        name=recipe.name,
        cuisine=recipe.cuisine,
        description=recipe.description,
        ingredients=[
            Ingredient(
                id=ingredient.id,
                name=ingredient.name,
                calories=ingredient.calories,
                unit=ingredient.unit,
                servingSize=ingredient.servingSize,
                carbohydrate=Carbohydrate(**ingredient.carbohydrate.model_dump()),
                fat=Fat(**ingredient.fat.model_dump()),
                protein=Protein(**ingredient.protein.model_dump()),
            )
            for ingredient in recipe.ingredients
        ],
    )
    return recipe


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_recipe(
        self,
        name: str,
        cuisine: str = "N/A",
        description: str = "",
        ingredients: List[BaseIngredient] = [],
    ) -> Recipe:
        queriedIngredients = await queryIngredients(ingredients)
        recipe = PydanticRecipe(
            name=name,
            cuisine=cuisine,
            description=description,
            ingredients=queriedIngredients,
        )
        addedRecipe = addRecipe(recipe)
        recipe = generateRecipeGraphQL(addedRecipe)
        return recipe

    @strawberry.mutation
    async def del_recipe(self, id: str) -> Recipe:
        deletedRecipe = delRecipe(id)
        recipe = generateRecipeGraphQL(deletedRecipe)
        return recipe

    @strawberry.mutation
    async def update_recipe(
        self,
        id: str,
        name: str = "",
        cuisine: str = "",
        description: str = "",
    ) -> Recipe:
        patch = Patch_Recipe(
            name=name,
            cuisine=cuisine,
            description=description,
        )
        updatedRecipe = updateRecipe(id=id, patchData=patch)
        recipe = generateRecipeGraphQL(updatedRecipe)
        return recipe

    @strawberry.mutation
    async def add_ingredients(
        self, id: str, ingredients: List[BaseIngredient] = []
    ) -> Recipe:
        if len(ingredients) == 0:
            return getRecipe(id)
        queriedIngredients = await queryIngredients(ingredients)
        updatedRecipe = addIngredients(id=id, ingredients=queriedIngredients)
        recipe = generateRecipeGraphQL(updatedRecipe)
        return recipe

    @strawberry.mutation
    async def del_ingredients(self, id: str, ingredients: List[str] = []) -> Recipe:
        if len(ingredients) == 0:
            return getRecipe(id)
        updatedRecipe = delIngredients(id=id, ingredientsToDelete=ingredients)
        recipe = generateRecipeGraphQL(updatedRecipe)
        return recipe

    @strawberry.mutation
    async def update_ingredients(
        self, id: str, ingredients: List[BaseIngredient] = []
    ) -> Recipe:
        queriedIngredients = await queryIngredients(ingredients)
        updatedRecipe = updateIngredients(id=id, ingredients=queriedIngredients)
        recipe = generateRecipeGraphQL(updatedRecipe)
        return recipe
