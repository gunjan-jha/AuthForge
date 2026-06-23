from datetime import datetime,timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_refresh_token, hash_password, verify_password,create_access_token
from app.repositories.user_repository import create_social_user, create_user, delete_refresh_token, get_refresh_token, get_user_by_email, get_user_by_id, save_refresh_token
from app.schemas.auth import RefreshRequest, SignupRequest
from app.core.oauth import oauth
auth_router=APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@auth_router.post("/login")
def login(form_data:OAuth2PasswordRequestForm= Depends(),
          db:Session=Depends(get_db)):
    """
    Fastapi standard oauth2 login flow
    """
    user = get_user_by_email(
        db,
        form_data.username
        )
    
    if not user:
        raise HTTPException(status_code=401,
                            detail="Invalid credentials")
    
    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
    data={
        "sub": str(user.id),
        "email": user.email,
        "role":user.role
    }
)
    refresh_token =create_refresh_token()
    save_refresh_token(
        db=db,
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow()+timedelta(days=30)
        )

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }


@auth_router.post("/signup")
def signup(
    payload:SignupRequest,
    db:Session=Depends(get_db)
):
    existing_user = get_user_by_email(db,payload.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(payload.password)
    user = create_user(
        db=db,
        email=payload.email,
        password_hash=hashed_password
    )

    access_token = create_access_token(
        data={
            "sub":str(user.id),
            "email":user.email,
            "role":user.role
        }
    )
    refresh_token = create_refresh_token()
    save_refresh_token(
        db=db,
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow()+timedelta(days=30)
        )

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer",
        "user":{
            "id":user.id,
            "email":user.email
        }
    }


@auth_router.get("/google/login")
async def google_login(
        request:Request
):
    redirect_uri=(
        "http://localhost:8000/auth/google/callback"
    )

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@auth_router.get("/google/callback")
async def google_callback(
    request:Request,
    db:Session=Depends(get_db)
):
    token =await  oauth.google.authorize_access_token(
        request
    )
    userinfo =token["userinfo"]
    email = userinfo["email"]
    google_id = userinfo["sub"]

    user = get_user_by_email(db,email)

    if not user:
        user = create_social_user(
            db=db,
            email=email,
            provider="google",
            provider_id=google_id
        )

        acess_token = create_access_token(
            {
                "sub":str(user.id),
                "role":user.role
            }
        )

        return {
            "acess_token":acess_token,
            "token_type":"bearer",
            "email":user.email
        }
    
@auth_router.post("/refresh")
def refresh_acess_token(
    payload: RefreshRequest,
    db:Session=Depends(get_db)
):
    token_record=get_refresh_token(
        db,
        payload.refresh_token
    )

    if not token_record:
        raise HTTPException(
            status_code=401,
            detail="Invalid Refresh token"
        )
    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail='Refresh token expired'
        )
    user =get_user_by_id(
       db,
       token_record.user_id
    )
    delete_refresh_token(db,payload.refresh_token)
    new_refresh_token=create_refresh_token()
    save_refresh_token(db=db,token=new_refresh_token,user_id=user.id,expires_at=datetime.utcnow()+timedelta(days=30))
    access_token = create_access_token(
        {
            "sub":str(user.id),
            "email":user.email,
            "role":user.role
        }
    )

    return {
        "access_token":access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer"
    }


@auth_router.post("/logout")
def logout(
    payload:RefreshRequest,
    db:Session=Depends(get_db)
):
    delete_refresh_token(db,payload.refresh_token)

    return{
        "message":"Logged out"
    }