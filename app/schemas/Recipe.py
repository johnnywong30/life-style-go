import strawberry
from app.models.Recipe import Recipe


@strawberry.experimental.pydantic.type(model=Recipe, all_fields=True)
class Recipe:
    pass
