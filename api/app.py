import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from routes import helpers, matches, players
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


from fastapi import FastAPI

app = FastAPI()
# Routers
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(helpers.router)


@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI on Vercel!"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
