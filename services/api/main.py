from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes import images_router, graphql_router
from api.broker import rabbit_connection


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    yield
    await rabbit_connection.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_router, prefix="/graphql")
app.include_router(images_router, prefix='', tags=['Images'])

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

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port=8000,
        log_level='debug',
        use_colors=True,
        host='0.0.0.0',
        reload=True
    )
