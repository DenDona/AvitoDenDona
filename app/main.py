from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import setup_dishka

from app.adapters.di.container import container
from app.cammon.exceptions import ApplicationError, RAMSException
from app.ports.rest.router import router as api_router


app = FastAPI(title="DenDona API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
setup_dishka(container=container, app=app)


@app.exception_handler(RAMSException)
async def rams_exception_handler(_: Request, exc: RAMSException) -> JSONResponse:
    payload = {"detail": str(exc)}
    if isinstance(exc, ApplicationError):
        payload["code"] = str(exc.code)
    return JSONResponse(status_code=exc.status_code, content=payload)
