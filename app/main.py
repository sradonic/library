from fastapi import FastAPI
from app.routers import user, auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)