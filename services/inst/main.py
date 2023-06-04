from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from inst.routers import auth_router, media_router, album_router

app = FastAPI(redoc_url=None, docs_url=None, openapi_url=None, title='Instagram Service')
app.include_router(auth_router)
app.include_router(media_router)
app.include_router(album_router)


@app.exception_handler(Exception)
async def handle_exception(_: Request, exc: Exception):
    return JSONResponse({
        "detail": str(exc),
        "exc_type": str(type(exc).__name__)
    }, status_code=500)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port=8000,
        log_level='debug',
        use_colors=True,
        host='0.0.0.0',
        reload=True
    )
