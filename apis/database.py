from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Corrected driver name: "mysql+pymysql"
DATABASE_URL = "mysql+pymysql://root:Waterquality01!@kayc0des.com/u58951209_waterquality"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

