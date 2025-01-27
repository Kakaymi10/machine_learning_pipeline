from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = "u58951209_group1"
host = "kayc0des.com"
database_name = "u58951209_waterquality"
password = "Waterquality01!"

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
