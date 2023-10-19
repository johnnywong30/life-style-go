from pydantic_redis import RedisConfig
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

CONFIG = RedisConfig(host=REDIS_HOST, port=REDIS_PORT)
EXPIRATION_TIME = 3600
STORE_NAME = "REDIS_STORE"
