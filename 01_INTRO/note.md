### What is SQL Alchemy?
- a db toolkit + an ORM 
- It has two parts which do these functionality, Core and ORM

### What is an ORM?
- Python Classes -> ORM -> SQL commands

### How to install?
- `Step-0` - make a virtual environment *(recommended)*
- `Step-1` - pip install sqlalchemy 
- `Step-2` - update requirements.txt *(If there is not one, create it, its a good practice ,even consider freezing the version)*

### How to create a Table?
- There is a general flow, make an engine.
- Have a declarative base and then create tables command.

### How to create an Engine?
- what is a engine? 
    - will discuss it later but till then its the first step to make a table

``` python
from sqlalchemy import create_engine

engine = create_engine(<db_url>)
```
### Whats a `db_url` and what to set there?

- every db has a url, sqlalchemy creates a db or connects to a db at that url
- url changes with different dbs but all of then have the same structure

```text
url looks like this : 

"<dialect>+<driver>://<username>:<password>@host:<port>/<database>"

# this is for reference, check out exact at sqlalchemy docs
```
- you can choose `sqlite`,`mysql`,`postgresql`
- for simplicity here we will choose sqlite
- later use the advance ones

### `db_url` for sqlite
- you can have a temporary memory one :
    - which exists till the program is running.
    ```python
    db_url = "sqlite://" #in memory 
    # check for the official docs for the exact one
    ```
- Or it can be persistant:
    - here it creates a .db file to store data
    - **Absolute Path vs Relative Path** 
    ```python
    db_url = "sqlite:////" # absolute path or
    db_url_anotherone = "sqlite:///" # relative one
    ```
### How engine connection code looks like?
```python
from sqlalchemy import create_engine
db_url = "sqlite:///database.db"
engine = create_engine(db_url)
```
- **Whats next ?** - have a base declared.

### Make a declarative base?
- *for know* ; its just used to create tables.
- these are used to create python classes which then are used to create tables.

```python
from sqlalchemy.orm import declarative_base()

## make engine then

Base = declarative_base()
Base.metadata.create_all(engine)
```
### How tables are created ?
- Tables are created via making classes.
```python
# make engine ,have Base, import Column,Integer,String from sqlalchemy

Class User(Base):
    __tablename__ = "users" # generally plural of the classname
    #essential - if not present ,throws an error 

    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)
# use Base.metadata.create_all(engine) // to create the table 
# the table will be empty. 
# we will learn CRUD next.
```
#### All these config are placed inside models.py in a general app to keep core logic in a different file.
---
