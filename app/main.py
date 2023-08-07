from fastapi import FastAPI

from app.api.api_v1 import api

app = FastAPI()

app.include_router(api.api_router, prefix='/api/v1/menus')
