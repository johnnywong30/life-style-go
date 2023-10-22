from app.data.mongo.connection import getMongoDB

mongo = getMongoDB()

RESULT_FILTER = {"_id": 0}

# TODO figure out the other collections
FOOD = mongo.food
RECIPE = mongo.recipe
