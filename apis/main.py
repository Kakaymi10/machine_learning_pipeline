from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

class LocationBase(BaseModel):
    location_id: int
    name: str
    longitude: float
    latitude: float
    adress: int

class UserBase(BaseModel):
    user_id: int
    name: str
    email: str
    profession: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
 