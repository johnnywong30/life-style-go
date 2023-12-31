from redis import Redis
from app.data.redis.config import REDIS_HOST, REDIS_PORT
from app.models.Ingredient import IngredientList
from app.models.Recipe import Recipe
import json


class RedisClient(Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.INGREDIENTS_KEY = "_INGREDIENTS"
        self.RECIPES_KEY = "_RECIPES"
        self.EXPIRATION_TIME = 3600

    def getIngredientKey(self, foodQuery: str) -> str:
        return f"{self.INGREDIENTS_KEY}/{foodQuery}"

    def getIngredients(self, foodQuery: str) -> IngredientList | None:
        """
        Gets IngredientList from cache using foodQuery as the Redis key.
        If the value does not exist, returns None.
        """
        key = self.getIngredientKey(foodQuery)
        ingredientsExist = self.exists(key)
        if not ingredientsExist:
            return None
        value = self.get(key)
        ingredientListDict = json.loads(value)
        # Update the expiration date on this value if it has less than 60 minutes left
        self.expire(name=key, time=self.EXPIRATION_TIME, gt=True)
        ingredients = IngredientList(**ingredientListDict)
        return ingredients

    def setIngredients(
        self,
        foodQuery: str,
        ingredients: IngredientList,
        expirationTime: int | None = None,
    ) -> IngredientList:
        """
        Caches ingredients by the key, value pair foodQuery:IngredientList.
        By default, these values expire every 60 minutes.
        """
        expirationTime = self.EXPIRATION_TIME if not expirationTime else expirationTime
        value = ingredients.model_dump_json()
        key = self.getIngredientKey(foodQuery)
        self.set(name=key, value=value)
        self.expire(name=key, time=expirationTime)
        return self.getIngredients(foodQuery)

    def getRecipe(self, recipeName: str) -> Recipe | None:
        """
        Gets Recipe from cache using recipeName as the Redis key.
        If the value does not exist, returns None.
        """
        key = recipeName
        recipeExists = self.exists(key)
        if not recipeExists:
            return None
        value = self.get(key)
        recipeDict = json.loads(value)
        # Update the expiration date on this value if it has less than 60 minutes left
        self.expire(name=key, time=self.EXPIRATION_TIME, gt=True)
        recipe = Recipe(**recipeDict)
        return recipe

    def setRecipe(self, recipe: Recipe, expirationTime: int | None = None) -> Recipe:
        """
        Caches recipes by the key, value pair recipe.name:recipe.
        By default, these values expire every 60 minutes.
        """
        expirationTime = self.EXPIRATION_TIME if not expirationTime else expirationTime
        EXCLUDE_FIELDS = ["carbohydrate", "fat", "protein"]
        value = recipe.model_dump_json(exclude=EXCLUDE_FIELDS)
        key = recipe.name
        self.set(name=key, value=value)
        self.expire(name=key, time=expirationTime)
        return self.getRecipe(recipe.name)

    def delRecipe(self, recipeName: str) -> Recipe | None:
        """
        Deletes Recipe from cache using recipeName as the Redis key.
        If the value does not exist, returns None
        """
        key = recipeName
        recipeExists = self.exists(key)
        if not recipeExists:
            return None
        value = self.get(key)
        recipeDict = json.loads(value)
        recipe = Recipe(**recipeDict)
        self.delete(key)
        return recipe
