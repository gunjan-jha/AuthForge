from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base,engine
from app.api.auth import auth_router
from app.api.users import router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command
# Base.metadata.create_all(bind=engine)
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://resilient-madeleine-73d809.netlify.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"]
)



def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

run_migrations()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET_KEY
)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)
app.include_router(
    router,
    prefix="/users",
    tags=["user"]
)
