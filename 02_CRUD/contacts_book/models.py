from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base

db_url = "sqlite:///contacts.db"

engine = create_engine(db_url)

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    category = Column(String)
    

Base.metadata.create_all(engine)

