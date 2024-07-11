from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

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

@app.post("/locations/", status_code = status.HTTP_201_CREATED)
async def create_locations(location: LocationBase, db: db_dependency):
    db_location = models.User(**location.dict())
    db.add(db_location)
    db.comit()

@app.get("/locations/{location_id}", status_code = status.HTTP_200_OK)
async def read_location(location_id: int, db: db_dependency):
    location= db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail= 'Location not found')
    return location

@app.delete("/locations/{location_id}", status_code = status.HTTP_200_OK)
async def delete_location(location_id: int, db: db_dependency):
    db_location= db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail= 'Location not found')
    db_location(db_location)
    db.commit()

@app.post("/users/", status_code = status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.comit()

@app.get("/users/{user_id}", status_code = status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user= db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail= 'User not found')
    return user

 