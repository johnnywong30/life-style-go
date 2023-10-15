import strawberry
from app.models.Ingredient import Ingredient, Macro, Carbohydrate, Fat, Protein


@strawberry.experimental.pydantic.type(model=Macro, all_fields=True)
class Macro:
    pass


@strawberry.experimental.pydantic.type(model=Carbohydrate, all_fields=True)
class Carbohydrate:
    pass


@strawberry.experimental.pydantic.type(model=Fat, all_fields=True)
class Fat:
    pass


@strawberry.experimental.pydantic.type(model=Protein, all_fields=True)
class Protein:
    pass


@strawberry.experimental.pydantic.type(model=Ingredient, all_fields=True)
class Ingredient:
    pass
