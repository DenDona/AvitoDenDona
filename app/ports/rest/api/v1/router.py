from fastapi import APIRouter

from app.ports.rest.api.v1.endpoints.auth import auth_router
from app.ports.rest.api.v1.endpoints.category import category_router
from app.ports.rest.api.v1.endpoints.chat import chat_router
from app.ports.rest.api.v1.endpoints.favorite import favorite_router
from app.ports.rest.api.v1.endpoints.post import post_router
from app.ports.rest.api.v1.endpoints.post_image import post_image_router
from app.ports.rest.api.v1.endpoints.review import review_router
from app.ports.rest.api.v1.endpoints.upload import upload_router
from app.ports.rest.api.v1.endpoints.users import user_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(post_router)
router.include_router(post_image_router)
router.include_router(upload_router)
router.include_router(favorite_router)
router.include_router(chat_router)
router.include_router(review_router)
router.include_router(category_router)