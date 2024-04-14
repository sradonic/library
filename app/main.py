from fastapi import FastAPI
from app.routers import user, auth, book
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI()
origins = settings.allow_origins.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)