import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")


DOCKER_MONGO_URI = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}/"
)


def getMongoClient(URI: str = DOCKER_MONGO_URI) -> pymongo.MongoClient:
    return pymongo.MongoClient(URI)


def getMongoDB(DB_NAME: str = MONGO_DB):
    return getMongoClient().get_database(DB_NAME)
