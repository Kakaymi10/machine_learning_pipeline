from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    profession = Column(String)
    

class Location(Base): 
    __tablename__ = "locattions"

    location_id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    address = Column(String, nullable=True)
