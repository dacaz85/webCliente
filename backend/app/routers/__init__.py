# app/routers/__init__.py
from .users import router as users_router
from .auth import router as auth_router
from .companies import router as companies_router
from .permissions import router as permissions_router

__all__ = ["users_router", "auth_router", "companies_router", "permissions_router"]
