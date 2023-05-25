from fastapi import FastAPI
from starlette.responses import JSONResponse
from routers import (
    auth, media, album
)


app = FastAPI()
app.include_router(auth.router)
app.include_router(media.router)
app.include_router(album.router)


@app.exception_handler(Exception)
async def handle_exception(request, exc: Exception):
    return JSONResponse({
        "detail": str(exc),
        "exc_type": str(type(exc).__name__)
    }, status_code=500)

