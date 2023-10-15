from app.data.mongo.connection import getMongoDB

mongo = getMongoDB()

RESULT_FILTER = {"_id": 0}

FOOD = mongo.food
# TODO figure out the other collections
