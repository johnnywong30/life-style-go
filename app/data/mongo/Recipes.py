from app.data.mongo import RECIPE, RESULT_FILTER
from typing import List
from app.models.Recipe import Recipe, Patch_Recipe
from app.models.Ingredient import Ingredient


def getRecipe(id: str) -> Recipe:
    recipeData = RECIPE.find_one({"id": id}, RESULT_FILTER)
    if not recipeData:
        raise Exception(f"Recipe with id {id} does not exist.")
    recipe = Recipe(**recipeData)
    return recipe


def addRecipe(recipe: Recipe) -> Recipe:
    recipeData = recipe.model_dump(mode="json")
    insertion = RECIPE.insert_one(recipeData)
    if not insertion.acknowledged:
        raise Exception(
            f"Unable to insert recipe for {recipe.name} with id {recipe.id}."
        )
    return getRecipe(id=recipe.id)


def delRecipe(id: str) -> Recipe:
    recipe = getRecipe(id)
    deletion = RECIPE.delete_one({"id": id})
    if not deletion.acknowledged:
        raise Exception(f"Unable to delete recipe with id {id}.")
    return recipe


def updateRecipe(id: str, patchData: Patch_Recipe) -> Recipe:
    recipe = getRecipe(id)
    newName, newCuisine, newDescription = (
        patchData.name,
        patchData.cuisine,
        patchData.description,
    )
    if not recipe.compareName(patchData):
        newName = recipe.name
    if not recipe.compareCuisine(patchData):
        newCuisine = recipe.cuisine
    if not recipe.compareDescription(patchData):
        newDescription = recipe.description
    update = RECIPE.update_one(
        {"id": id},
        {
            "$set": {
                "name": newName,
                "cuisine": newCuisine,
                "description": newDescription,
            }
        },
    )
    if not update.acknowledged:
        raise Exception(f"Unable to update recipe with id {id}.")
    return getRecipe(id)


def addIngredients(id: str, ingredients: List[Ingredient]) -> Recipe:
    recipe = getRecipe(id)
    ingredients = [
        ingredient.model_dump(mode="json")
        for ingredient in ingredients
        if ingredient.id not in [ingredient.id for ingredient in recipe.ingredients]
    ]
    update = RECIPE.update_one(
        {"id": id},
        {"$push": {"ingredients": {"$each": ingredients}}},
    )
    if not update.acknowledged:
        raise Exception(f"Unable to add ingredients to recipe with id {id}.")
    return getRecipe(id)


def delIngredients(id: str, ingredientsToDelete: List[str]) -> Recipe:
    recipe = getRecipe(id)
    ingredients = [
        ingredient.model_dump(mode="json")
        for ingredient in recipe.ingredients
        if ingredient.id not in ingredientsToDelete
    ]
    update = RECIPE.update_one({"id": id}, {"$set": {"ingredients": ingredients}})
    if not update.acknowledged:
        raise Exception(f"Unable to delete ingredients from recipe with id {id}.")
    recipe = getRecipe(id)
    return recipe


def updateIngredients(id: str, ingredients: List[Ingredient]) -> Recipe:
    recipe = getRecipe(id)
    ingredients = [ingredient.model_dump(mode="json") for ingredient in ingredients]
    update = RECIPE.update_one({"id": id}, {"$set": {"ingredients": ingredients}})
    if not update.acknowledged:
        raise Exception(f"Unable to update ingredients in recipe with id {id}.")
    recipe = getRecipe(id)
    return recipe
