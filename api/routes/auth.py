# import datetime
# import os
# from contextvars import Token
# from typing import Annotated

# from auth.security import (
#     ACCESS_TOKEN_EXPIRE_MINUTES,
#     authenticate_user,
#     create_access_token,
#     fake_users_db,
#     get_current_active_user,
# )
# from dotenv import load_dotenv
# from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from routes import helpers, matches, players
# from schemas.token import Token
# from schemas.user import User
# from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, text
# from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

# router = APIRouter(prefix="/auth", tags=["auth"])


# @router.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return Token(access_token=access_token, token_type="bearer")


# @router.get("/users/me")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user
