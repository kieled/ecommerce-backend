from contextlib import asynccontextmanager

import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig

from graph import Query, Mutation
from router import router
from utils import get_context
from api.config import rabbit_connection

strawberry_config = StrawberryConfig(auto_camel_case=True)

schema = strawberry.Schema(Query, Mutation, config=strawberry_config)
graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    yield
    await rabbit_connection.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
app.include_router(router, prefix='', tags=['Api'])

origins = [
    "http://localhost:3000",
    "http://app:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/images', StaticFiles(directory="assets/aliexpress"), name="images")
app.mount('/temp', StaticFiles(directory="assets/temp"), name="temp_images")
