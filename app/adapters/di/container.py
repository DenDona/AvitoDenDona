from dishka import make_async_container

from app.adapters.di.providers.auth import AuthProvider
from app.adapters.di.providers.category import CategoryProvider
from app.adapters.di.providers.post import PostProvider
from app.adapters.di.providers.post_image import PostImageProvider
from app.adapters.di.providers.session import SessionProvider
from app.adapters.di.providers.user import UserProvider

container = make_async_container(
    SessionProvider(), AuthProvider(), PostProvider(), UserProvider(),
    CategoryProvider(), PostImageProvider(),
)