
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    decode_access_token,
)
from app.repositories.user_repository import (
    get_user_by_id,
)
from app.api.auth import oauth2_scheme


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def require_role(required_role:str):
    def checker(
            current_user=Depends(get_current_user)
    ):
        print("current role --",current_user.role)
        if current_user.role!=required_role:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )
        return current_user
    
    return checker