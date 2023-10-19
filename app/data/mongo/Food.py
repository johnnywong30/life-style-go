from app.externalModels.ninjaNutrients.Ingredient import NinjaFood, NinjaNutritionResult
from app.data.mongo import FOOD, RESULT_FILTER
from typing import List, Dict


def getFoods(query: str) -> List[NinjaFood]:
    """
    Get List of NinjaFood from MongoDB corresponding to exact query
    """
    foodFilter: Dict[str, str] = {"query": query}
    response = FOOD.find_one(foodFilter, RESULT_FILTER)
    if not response:
        return []
    result = NinjaNutritionResult(**response)
    foods = result.foods
    return foods


def addFoods(query: str, foods: List[NinjaFood]) -> List[NinjaFood]:
    """
    Add List of NinjaFood to MongoDB, using the query as the Primary Key
    """
    result = NinjaNutritionResult(query=query, foods=foods)
    response = FOOD.insert_one(result.model_dump(mode="json"))
    if not response.acknowledged:
        raise Exception(f"Could not insert food from query {query} into MongoDB.")
    return getFoods(query)


# Should not need to delete at any point?
def delFoods(query: str) -> List[NinjaFood]:
    """
    Delete List of NinjaFood from MongoDB, using the query as the Primary Key
    """
    foods = getFoods(query)
    foodFilter: Dict[str, str] = {"query": query}
    response = FOOD.delete_one(foodFilter)
    if not response.acknowledged:
        raise Exception(f"Could not delete food from query {query} in MongoDB.")
    return foods
