from fastapi import APIRouter

from app.ports.rest.api.v1.endpoints.auth import auth_router
from app.ports.rest.api.v1.endpoints.post import post_router
from app.ports.rest.api.v1.endpoints.users import user_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(post_router)
