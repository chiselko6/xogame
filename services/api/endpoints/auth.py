from typing import Optional
from db.client import DBClient
from datetime import datetime, timedelta
from db.schemas.auth import Token as TokenSchema
from db.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from settings import Config

app = FastAPI()

db_client = DBClient()
db_client.init()

config = Config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = db_client.get_user(username)
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=config.jwt_token_access_expire_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, config.jwt_token_secret_key, algorithm=config.jwt_token_algorithm)


@app.post("/token", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
