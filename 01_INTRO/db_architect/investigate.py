from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base
import os

current_dir=os.path.abspath(os.path.dirname(__file__))
print(os.path.dirname(__file__))
db_path = os.path.join(current_dir,"db.db")
db_url = f"sqlite:///{db_path}"


# sqlite in-memory db

engine_memory = create_engine("sqlite://")

Base_A = declarative_base()

class User(Base_A):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String)

Base_A.metadata.create_all(engine_memory)
print("In memory db created.")

engine_relative = create_engine("sqlite:///database.db")

Base_B = declarative_base()

class User(Base_B):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String)

Base_B.metadata.create_all(engine_relative)
print("database.db created in the same folder")

engine_absolute = create_engine(db_url)

Base_C = declarative_base()

class User(Base_C):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String)

Base_C.metadata.create_all(engine_absolute)
print(f"db.db created in {db_path}")

