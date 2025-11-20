from fastapi import FastAPI, Body,Depends,Response
from app.models import User
from app.schema import UserSchema,UserLoginSchema,SentimentRequest,SentimentResponse,TokenData
from app.auth.jwt_handler import signJWT ,get_current_user
from app.auth.auth_router import check_user
from sqlalchemy.orm import Session 
from app.database import get_db
from app.database import engine , Base
from app.services.huggingface_service import predict_sentiment
app = FastAPI(
    description="API d'analyse de sentiment avec authentification JWT"
)
Base.metadata.create_all(bind=engine)

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...),db:Session=Depends(get_db)):
    new_User=User(
        email=user.email,
        password=user.password,
    )
    db.add(new_User) 
    db.commit()
    db.refresh(new_User)
    return 'sign up succesfully'

@app.post("/user/login", tags=["user"])
async def user_login(response: Response,user: UserLoginSchema = Body(...),db:Session=Depends(get_db)):
    if check_user(user ,db):
        token = signJWT(user.email)
        response.set_cookie(
        key="access_token",
        value=token['access_token'],
        httponly=True,        # JS cannot read it (more secure)
        samesite="lax",       # or "strict" or "none"
        secure=False          # True in production (requires HTTPS)
    )
        return {'message':'login sucessfull',
                'token':token}

    return {
        "error": "Wrong login details!"
    }
@app.post("/predict", response_model=SentimentResponse)
async def predict(request: SentimentRequest, current_user: TokenData = Depends(get_current_user)):
    result = await predict_sentiment(request.text)
    return SentimentResponse(text=request.text, **result)

       
