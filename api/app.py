import datetime
import os
from contextvars import Token
from typing import Annotated

from auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    fake_users_db,
    get_current_active_user,
)
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes import helpers, matches, players
from schemas.token import Token
from schemas.user import User
from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, text
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

load_dotenv()  # loads .env into environment variables

DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_ID = os.environ["DB_ID"]
DB_URL = os.environ["DB_URL"]
DB_PORT = os.environ.get("DB_PORT")


connection_string = f"postgresql://postgres.{DB_ID}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/postgres"

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# --- DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

# Routers
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(helpers.router)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI on Vercel!"}


@app.get("/api/health")
def health_check(current_user: User = Depends(get_current_active_user)):

    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
