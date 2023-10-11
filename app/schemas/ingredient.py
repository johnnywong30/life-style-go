import strawberry
from app.models.Ingredient import Ingredient


@strawberry.experimental.pydantic.type(model=Ingredient, all_fields=True)
class Ingredient:
    pass
