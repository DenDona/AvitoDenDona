import uuid
from pathlib import Path
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from starlette.requests import Request

from app.application.services.auth_service import AuthService
from app.config import settings
from app.ports.rest.api.v1.schema import BaseSchema

upload_router = APIRouter(prefix="/upload", tags=["upload"], route_class=DishkaRoute)
bearer_scheme = HTTPBearer()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class UploadResponseSchema(BaseSchema):
    url: str


@upload_router.post("/image", response_model=UploadResponseSchema, status_code=status.HTTP_201_CREATED)
async def upload_image(
        request: Request,
        auth_service: FromDishka[AuthService],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
        file: UploadFile = File(...),
) -> UploadResponseSchema:
    await auth_service.get_user_from_token(credentials.credentials)

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    ext = Path(file.filename or "image.jpg").suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"

    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    (upload_path / filename).write_bytes(content)

    base_url = str(request.base_url).rstrip("/")
    return UploadResponseSchema(url=f"{base_url}/static/{filename}")