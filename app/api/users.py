from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import get_all_users, get_user_by_id
router = APIRouter(
    tags=["Users"]
)


@router.put("/{user_id}/make-admin")
def make_admin(
        user_id:str,
        db:Session=Depends(get_db),
        current_user=Depends(require_role("admin"))
):
    user = get_user_by_id(db,user_id)

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    #update role
    user.role ="admin"
    db.commit()
    db.refresh(user)

    return {
        "message":"User Promoted to admin successfully",
        "user_id":user.id,
        "role":user.role
    }
    
@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
    )
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "provider": current_user.provider,
        "Role":current_user.role
    }


@router.get("/admin")
def admin_dashboard(
    current_user=Depends(
        require_role("admin")
    )
):
    return {
        "message":"Welcome admin"
    }

@router.get("/all-users")
def get_all(current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.put("{user_id}/make-admin")
def make_admin(
        user_id:str,
        db:Session=Depends(get_db),
        current_user=Depends(require_role("admin"))
):
    user = get_user_by_id(db,user_id)

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    #update role
    user.role ="admin"
    db.commit()
    db.refresh(user)

    return {
        "message":"User Promoted to admin successfully",
        "user_id":user.id,
        "role":user.role
    }
    