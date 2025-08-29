from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship

engine = create_engine("sqlite:///blog.db")
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer,primary_key=True)

class User(BaseModel):
    __tablename__ = "users"
    username = Column(String,unique=True)
    posts = relationship("Post",back_populates="author")

class Post(BaseModel):
    __tablename__ = "posts"
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

Base.metadata.create_all(engine)