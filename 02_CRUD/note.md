## CRUD

- All the part of code with engine and declarative base in kept in a separate file called `models.py`

### Create

```python
from model import User,engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

user = User(name="Somu",age=19)
session.add(user)
session.commit()
```
- If we have multiple `user` then we can use `add_all()`
```python
# all imports and previous code
User_1 = User(name="Steve",age=24)
User_2 = User(name="John",age=73)
User_3 = User(name="Jane",age=49)
User_4 = User(name="Marshal",age=19)

session.add_all([User_1,User_2,User_3,User_4])
session.commit()
```
### Read
```python
users = session.query(User).all()
print(user)
print(user[0])
print(f"{user[0].name} - {user[0].age}")
```
- use `filter_by()` to get a filtered data
```python
user = session.query(User).filter_by(id=1).all()
```
- If query provides only one unique value, we can use `.one_or_none()`
```python
user = session.query(User).filter_by(id=1).one_or_none()
```
### Update
- After reading, we can update via simple python logic.
- If want to update `id=1` query 
```python
user = session.query(User).filter_by(id=1).one_or_none()
user.name = "Robert"
user.age = 42
user.commit() #make sure you commit
```
### Delete
- If I want to delete the user from the above example we can do it in this way.
```python
session.delete(user)
session.commit()
```
---
