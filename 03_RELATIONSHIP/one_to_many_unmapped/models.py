from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base,relationship
db_url = "sqlite:///db.db"

engine = create_engine(db_url)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer,primary_key=True)

class Address(BaseModel):
    __tablename__ = "addresses"
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User",back_populates="addresses")
    def __repr__(self):
        return f"<Address(city={self.city},state={self.state},zip_code={self.zip_code},user_id={self.user_id},user={self.user})>"

class User(BaseModel):
    __tablename__ = "users"
    name = Column(String)
    age = Column(Integer)
    addresses = relationship("Address")
    def __repr__(self):
        return f"<User(name={self.name},age={self.age},addresses={self.addresses})"
    
Base.metadata.create_all(engine)