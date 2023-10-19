from enum import Enum


class INGREDIENT_UNIT(Enum):
    g = "g"
    kg = "kg"
    oz = "oz"
    lb = "lb"
    cup = "cup"
    ml = "ml"
    l = "l"
    tsp = "tsp"
    tbsp = "tbsp"


class INGREDIENT_CATEGORY(Enum):
    meat = "Meat"
    vegetable = "Vegetable"
    fruit = "Fruit"
    carbohydrate = "Carbohydrate"
