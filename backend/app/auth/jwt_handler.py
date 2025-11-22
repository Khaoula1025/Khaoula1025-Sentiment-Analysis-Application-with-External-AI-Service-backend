import time
from jose import jwt,JWTError
from fastapi import Depends, HTTPException
from decouple import config
from dotenv import load_dotenv
import os
load_dotenv()
JWT_SECRET = os.getenv("secret")
JWT_ALGORITHM = 'HS256'

from fastapi.security import APIKeyCookie

# api_key_cookie = APIKeyCookie(name="access_token")
from fastapi import Cookie, HTTPException

def api_key_cookie(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return access_token

def signJWT(user_id: str) :
    payload = {
        "user_id": user_id,
        "expires": time.time() + 900
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(api_key_cookie)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")