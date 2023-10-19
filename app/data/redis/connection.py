from pydantic_redis import Store, Model, RedisConfig
from app.data.redis.config import CONFIG
from pydantic import Field
from typing import List, Annotated

from app.models.Ingredient import (
    Macro,
    Carbohydrate,
    Fat,
    Protein,
    Ingredient,
    IngredientList,
)

MODELS: List[Model] = [
    Macro,
    Carbohydrate,
    Fat,
    Protein,
    Ingredient,
    IngredientList,
]


class RedisStore:
    def __init__(
        self,
        models: List[Model],
        name: str = "Redis Store",
        redis_config: RedisConfig = CONFIG,
        model_expiration: Annotated[
            int, Field(description="Number of seconds till value expires")
        ] = 3600,
    ):
        self.name = name
        self.models = models
        self.redis_config = redis_config
        self.model_expiration = model_expiration

    def getStore(self):
        redis_store = Store(
            name=self.name,
            redis_config=self.redis_config,
            life_span_in_seconds=self.model_expiration,
        )
        for model in self.models:
            redis_store.register_model(model)
        redis_store.model_rebuild()
        return redis_store
