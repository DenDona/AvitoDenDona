from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dishka.integrations.fastapi import setup_dishka

from app.adapters.di.container import container
from app.cammon.exceptions import ApplicationError, RAMSException
from app.config import settings
from app.ports.rest.router import router as api_router


app = FastAPI(title="DenDona API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_path = Path(settings.upload_dir)
upload_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(upload_path)), name="static")

app.include_router(api_router)
setup_dishka(container=container, app=app)


@app.exception_handler(RAMSException)
async def rams_exception_handler(_: Request, exc: RAMSException) -> JSONResponse:
    payload = {"detail": str(exc)}
    if isinstance(exc, ApplicationError):
        payload["code"] = str(exc.code)
    return JSONResponse(status_code=exc.status_code, content=payload)
