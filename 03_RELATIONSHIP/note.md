### Relationships in SQL
- there are two ways
    1. Mapped
    2. Unmapped

### One to Many Relationship
- First we create a BaseModel
```python
class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer,primary_key = True)

class Address(BaseModel):
    __tablename__ = "addresses"
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    user_id = Column(ForeignKey("users.id"))
    def __repr__(self):
        return f"<Address(city={self.city},state={self.city},zip_code={self.zip_code},user_id='{self.user_id}')>"


class User(BaseModel):
    __tablename__ = "users"
    name = Column(String)
    age = Column(Integer)
    addresses = relationship(Address)
    def __repr__(self):
        return f"<User(id={self.id},username='{self.name}')>"
```
---
```python

# non mapped
class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer,primary_key=True)

class Address(BaseModel):
     __tablename__ = "addresses"
     city = Column(String)
     state = Column(String)
     zip_code = Column(Integer)
     user_id = Column(ForeignKey("users.id"))
     user =  relationship("User",back_populates="addresses")

class User(BaseModel):
     __tablename__ = "users"
     name = Column(String)
     age = Column(Integer)
     addresses = relationship(Address)



Base.metadata.create_all(engine)
```
```python
# mapped
class Address(BaseModel):
     __tablename__ = "addresses"
     city = Column(String)
     state = Column(String)
     zip_code = Column(Integer)
     user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
     user:Mapped["User"] =  relationship(back_populates="addresses")

class User(BaseModel):
     __tablename__ = "users"
     name = Column(String)
     age = Column(Integer)
     addresses:Mapped[list["Address"]] = relationship()



Base.metadata.create_all(engine)
```
### self-relationship
```python
class User(Base):
     __tablename__ = "users"
     __allow_unmapped__ = True
     id = Column(Integer,primary_key=True)
     username = Column(String)
     following_id = Column(Integer,ForeignKey('users.id'))
     following = relationship('User',remote_side = [id],uselist= True)
     def __repr__(self):
          return f"<User(id='{self.id}',username='{self.username},following={self.following}')"


Base.metadata.create_all(engine)

```

### Circular dependency may occur in a self-referencing table
- hence have an association table
```python

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
```

---
### One to One relationship
```python
from sqlalchemy import Column,ForeignKey,Integer,String,create_engine

from sqlalchemy.orm import declarative_base,relationship,sessionmaker

db_url="sqlite:///database.db"

engine=create_engine(db_url)
Base=declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    address = relationship("Address",back_populates="user",uselist=False)

class Address(Base):
    __tablename__ ="addresses"
    id = Column(Integer,primary_key=True)
    email = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User",back_populates="address")

Base.metadata.create_all(engine)

# new_user = User(name="John")
# new_Address = Address(email="john@example.com",user = new_user)

# session.add(new_user)
# session.add(new_Address)

# session.commit()

user = session.query(User).filter_by(name="John").first()
print(f"{user.id}   {user.name}   {user.address.email}")
```
### Self relationship
```python
from sqlalchemy import Column,ForeignKey,Integer,String,create_engine

from sqlalchemy.orm import declarative_base,relationship,sessionmaker

db_url="sqlite:///database.db"

engine=create_engine(db_url)
Base=declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class NodeAssociation(Base):
    __tablename__ ="node_associations"
    id = Column(Integer,primary_key=True)
    current_node_id = Column(Integer,ForeignKey("nodes.id"))
    next_node_id = Column(Integer,ForeignKey('nodes.id'))

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer,primary_key=True)
    value = Column(Integer,nullable=False)
    next_node = relationship("Node",secondary="node_associations",primaryjoin="NodeAssociation.current_node_id == Node.id",secondaryjoin="NodeAssociation.next_node_id ==Node.id",uselist=False)

    def __repr__(self):
        return f"<Node value={self.value}>"
    
Base.metadata.create_all(engine)

node1 = Node(value=1)
node2 = Node(value=2)
node3 = Node(value=3)

node1.next_node = node2
node2.next_node = node3

session.add_all([node1,node2,node3])
session.commit()

print(node1)
print(node2)
print(node3)
```