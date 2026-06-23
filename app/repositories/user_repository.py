from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from app.models.user import User


def get_user_by_email(db:Session,email:str):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def create_user(
        db:Session,
        email:str,
        password_hash:str
):
    user = User(
        email=email,
        password_hash=password_hash,
        provider="local"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(
        db,
        user_id:str
):
    return(
        db.query(User)
        .filter(User.id==user_id)
        .first()
    )

def get_all_users(
        db
):
    users=db.query(User).all()
    return [{"id":u.id,"email":u.email,"role":u.role} for u in users ]


def create_social_user(
        db,
        email:str,
        provider:str,
        provider_id:str
):
    user=User(
        email=email,
        provider=provider,
        provider_id=provider_id,
        password_hash=None
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def save_refresh_token(db,
                       token,
                       user_id,
                       expires_at):
    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_refresh_token(
        db,
        token
):
    return(
        db.query(RefreshToken)
        .filter(
            RefreshToken.token==token
        ).first()
    )

def delete_refresh_token(
        db,
        token
        ):
    db.query(RefreshToken).filter(RefreshToken.token==token).delete()
    db.commit()