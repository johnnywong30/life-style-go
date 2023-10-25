from pydantic import BaseModel, computed_field, Field
from app.models.Ingredient import Ingredient, Carbohydrate, Fat, Protein
from typing import List
from app.models import ID_Factory
from app.shared.validators import validString


class Patch_Recipe(BaseModel):
    name: str = ""
    cuisine: str = "N/A"
    description: str = ""


class Recipe(Patch_Recipe):
    id: str = Field(default_factory=ID_Factory)
    ingredients: List[Ingredient] = []

    @computed_field
    @property
    def carbohydrate(self) -> Carbohydrate:
        total = sum([ingredient.carbohydrate.amount for ingredient in self.ingredients])
        return Carbohydrate(amount=total)

    @computed_field
    @property
    def fat(self) -> Fat:
        total = sum([ingredient.fat.amount for ingredient in self.ingredients])
        return Fat(amount=total)

    @computed_field
    @property
    def protein(self) -> Protein:
        total = sum([ingredient.protein.amount for ingredient in self.ingredients])
        return Protein(amount=total)

    def compareName(self, patchData: Patch_Recipe) -> bool:
        newName = patchData.name
        return (
            validString(newName)
            and newName.strip().lower() != self.name.strip().lower()
        )

    def compareCuisine(self, patchData: Patch_Recipe) -> bool:
        newCuisine = patchData.cuisine
        return (
            validString(newCuisine)
            and newCuisine.strip().lower() != self.cuisine.strip().lower()
        )

    def compareDescription(self, patchData: Patch_Recipe) -> bool:
        newDescription = patchData.description
        return (
            validString(newDescription)
            and newDescription.strip().lower() != self.description.strip().lower()
        )
