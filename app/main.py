
from fastapi import FastAPI
from .middlewares import AuthMiddleware
from .routers import unlock, health


app = FastAPI(title="PDF Unlock API")
app.add_middleware(AuthMiddleware)


app.include_router(unlock.router)
app.include_router(health.router)