from fastapi import APIRouter

from .routers import dishes, menus, submenus

api_router = APIRouter()
api_router.include_router(menus.router)
api_router.include_router(submenus.router)
api_router.include_router(dishes.router)
