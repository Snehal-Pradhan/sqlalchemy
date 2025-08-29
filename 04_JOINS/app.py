from sqlalchemy import create_engine,ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,sessionmaker
from typing import Optional

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()
class Base(DeclarativeBase):
    id:Mapped[int] = mapped_column(primary_key=True)

class Address(Base):
    __tablename__ = "addresses"
    user_id:Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    data:Mapped[str]

    def __repr__(self) ->str:
        return f"< Address: {self.data}>"
    
class User(Base):
    __tablename__ = "users"
    first_name:Mapped[str]
    last_name:Mapped[str]
    address:Mapped[Address] = relationship()

    def __repr__(self):
        return f"< User: {self.first_name} {self.last_name}>"


Base.metadata.create_all(engine)

"""

address_1 = Address(data="1000 random address")
address_2 = Address(data="1001 random address")
address_3 = Address(data="1002 random address")

user_1 = User(
    first_name="Alex",
    last_name="Mercer",
    address=address_1
)
user_2 = User(
    first_name="John",
    last_name="Doe",
    address =None
)

session.add_all([address_1,address_2,address_3,user_1,user_2])

session.commit()
session.close()
"""

# INNER JOIN
# result = session.query(User,Address).join(Address).all()
# print("\nInner Join")
# print(result)

# ANTI INNER JOIN
result = session.query(User).join(Address,full=True).filter(User.address==None,Address.user_id==None).all()
print(result)