from fastapi import FastAPI
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from app.externalModels.ninjaNutrients.Ingredient import NinjaNutritionClient

app = FastAPI()

# graphqlApp = GraphQLRouter()
# app.include_router(graphqlApp, prefix="/graphql")


@app.get("/")
async def root():
    return JSONResponse(content="Hello")


@app.get("/test")
async def food(searchTerm: str):
    client = NinjaNutritionClient()
    content = await client.query(searchTerm)
    return JSONResponse(content)


# @app.get("/food/{id}")
# async def food(id: str):
#     content = await getFood(id)
#     return JSONResponse(content)
