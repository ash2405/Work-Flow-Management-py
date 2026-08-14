from pwdlib import PasswordHash
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException,status
import jwt

from app.core.config import settings


password_hash = PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)


def verify_password(password:str, hashed:str)-> str:
    return password_hash.verify(password,hashed)

def create_access_token(
        user_id:int,
        expires_delta: timedelta | None ='None'
):

    expires = datetime.now(
        timezone.utc
    ) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 

    payload = {
        "sub":str(user_id),
        "exp":expires,
        "type":"access"
     }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def create_refresh_token(user_id:int):

    expire = datetime(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub":int(user_id),
        "exp":expire,
        "type":"refresh"
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_access_token(token:str):
    try:
        payload = jwt.decode(
            token,
            jwt=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )

def decode_refresh_token(token:str):
    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get('type') != 'refresh':
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token refresh"
            )
        
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token has"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )