import strawberry
from app.models.Recipe import Recipe, Patch_Recipe
from app.models.Ingredient import Ingredient
from app.data.mongo.Recipes import (
    getRecipe,
    addRecipe,
    delRecipe,
    updateRecipe,
    addIngredients,
    delIngredients,
    updateIngredients,
)


@strawberry.type
# TODO
class Mutation:
    @strawberry.mutation
    def add_recipe(self) -> Recipe:
        pass

    @strawberry.mutation
    def del_recipe(self, id: str) -> Recipe:
        pass

    @strawberry.mutation
    def update_recipe(self) -> Recipe:
        pass

    @strawberry.mutation
    def add_ingredients(self) -> Recipe:
        pass

    @strawberry.mutation
    def del_ingredients(self) -> Recipe:
        pass

    @strawberry.mutation
    def update_ingredients(self) -> Recipe:
        pass
