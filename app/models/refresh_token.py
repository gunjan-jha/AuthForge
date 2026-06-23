from sqlalchemy import Boolean, DateTime, ForeignKey, String
from app.core.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime


class RefreshToken(Base):
    __tablename__ ="refresh_tokens"
    id:Mapped[int]= mapped_column(primary_key=True)
    token:Mapped[str]=mapped_column(
        String,
        unique=True,
        index=True
    )
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id")
    )
    expires_at:Mapped[datetime]=mapped_column(
        DateTime
    )
    revoked:Mapped[Boolean]=mapped_column(Boolean,default=False)