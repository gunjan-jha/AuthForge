from uuid import uuid4
from sqlalchemy import DateTime, String, func
from app.core.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base

class User(Base):
    __tablename__="users"
    id:Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda:str(uuid4())
        )
    email:Mapped[str]=mapped_column(
        String(255),
        unique=True,
        index=True
    )
    password_hash:Mapped[str|None]=mapped_column(
        String(255),
        nullable=True
    )
    provider:Mapped[str]=mapped_column(
        String(50),
        default="local"
        )
    provider_id:Mapped[str|None]=mapped_column(
        String(255),
        nullable=True
    )
    created_at: Mapped[str] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
)
    role:Mapped[str]=mapped_column(
        String(255),
        nullable=False,
        default="user"
    )
