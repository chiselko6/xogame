from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from db.client import DBClient
from db.models import User
from settings import Config

from .schemas import AuthTokenData, IntraTokenData, Token, TokenType
from .util import decode_auth_token, encode_auth_token, encode_intra_token

app = FastAPI()

db_client = DBClient()
db_client.init()

config = Config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare the passwords using hash"""

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


@app.get("/intratoken/{game_uuid}", response_model=Token)
async def get_intra_token(game_uuid: UUID, token: str = Depends(oauth2_scheme)):
    """Exchange Bearer token to intratoken."""

    decoded = decode_auth_token(token)
    return Token(
        access_token=encode_intra_token(decoded.username, game_uuid),
        token_type=TokenType.INTRA,
    )


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to the app and receive a Bearer token"""

    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encode_auth_token(username=user.username)
    return Token(access_token=access_token, token_type=TokenType.BEARER)
