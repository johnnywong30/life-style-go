import strawberry
from app.schemas import Ingredient

# from app.externalModels.fdcModels import FDC_URL, FDC_FOOD_URL, FDC_KEY
# from app.externalModels.fdcModels.Food import Food
from app.shared.helpers import AsyncClient

# import redis


@strawberry.type
class Ingredient_Query:
    #  Ingredient: Ingredient = strawberry.field(resolver=getFDCIngredient)
    Ingredient: Ingredient
