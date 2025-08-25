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
### Ordering Data
Here for example we have fake data.
```python 
name = ["a","b","c","d","e","f","g","h"]
age = [19,23,45,36,49,75,85,57]
import random
for i in range(20):
    user = User(name=random.choice(name),age=random.choice(age))
    session.add(user)
session.commit()
```
- Ordering can be done by age (default is ascending order.)
```python
user=session.query(User).order_by(User.age).all()
```
- Can be done in descending order by `.desc()`
```python
session.query(User).order_by(User.age.desc()).all()
```
- can also have multiple values
```python
session.query(User).order_by(User.age,User.name).all()
```
### Filtering
```python
user_all = session.query(User).all()
user_filtered = session.query(User).filter(User.age>=25).all()
```
```python
.filter(User.age>=25,Username=="Snehal")
```
- `.where()` works similarly.
```python
user = session.query(User).where(User.age >= 30).all()
user2 = session.query(User).where(User.age >= 30,User.name =="").all()
```
- we can have `or_` statements `and_` statements are default.
- also `not_` is present.
```python
from sqlalchemy import or_,and_
##
.where(or_(User.age >=30 ,User.name =="Ironman")).all()
##
.where((User.age >=30)|(User.name =="Ironman")).all()
##
.where(and_(User.age >=30 ,User.name =="Ironman")).all()
##
.where((User.age >=30)&(User.name =="Ironman")).all()
##
.where(not_(name=="Somu")).all()
```
### Grouping
```python
session=session.query(User).group_by(User.age).all()
## puts together users with unique age.
```
- we can add a `func` function which will count the number of users.
```python
from sqlalchemy import func
users=session.query(User.age,func.count(User.id)).group_by(User.age).all()
```

### Chaining
```python
users = session.query(User).filter(User.age > 30).filter(User.age < 50).all()
```

### Conditional grouping
```python
only_iron_man = True
group_by_age = True
users =  session.query(User)
if only_iron_man:
    users = users.filter(User.name =="Iron Man")
if group_by_age:
    users = users.group_by(User.age)
users = users.all()
```