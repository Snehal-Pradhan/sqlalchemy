### Indexes
- It is a datastructure which improves the retrieval operation on a data table at the cost of additional writes and storage space
- uses binary tree in the background
- frequent searches,joins,filtering,sorting,constraints and uniques
#### When no to use
- small data table
- heavy write operations , or batch operations

 ```python

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine, String, Sequence
import time

# Set up the SQLite database
engine = create_engine('sqlite:///example.db', echo=False)

# Optional set to memory instead of a file
# engine = create_engine('sqlite:///:memory:', echo=False)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Sequence('id_seq'), primary_key=True)


class WithoutIndex(Base):
    __tablename__ = 'without_index'
    data: Mapped[str] = mapped_column(String(50))


class WithIndex(Base):
    __tablename__ = 'with_index'
    data: Mapped[str] = mapped_column(String(50), index=True)


# Database connection
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

# Create session
s = sessionmaker(bind=engine)
session: Session = s()


# Function to insert data into a table
def insert_data(session: Session, model: WithoutIndex | WithIndex, num_rows: int):
    start_time = time.perf_counter()
    models = []
    for i in range(num_rows):
        if i % 10_000 == 0:
            print(f'\r{i:>10,} / {num_rows:,}', end='\r')
            session.bulk_save_objects(models)
            models = []

        models.append(model(data=f'data_{i}'))

    session.bulk_save_objects(models)
    session.commit()
    end_time = time.perf_counter()
    return round(end_time - start_time, 4)


def fetch_data(session: Session, model: WithoutIndex | WithIndex):
    start_time = time.perf_counter()
    data = session.query(model).filter(model.data == 'data_5343').first()
    end_time = time.perf_counter()
    return round(end_time - start_time, 4)


def calc_time(start, end):
    value = round((end - start) / start, 2) * 100
    return abs(value)


# =============================================================
#                       INSERTING DATA
# =============================================================
# Insert data into table without index
num_rows = 500_000
print(f'Writing Data - {num_rows:,} rows without an index')
time_without_index = insert_data(session, WithoutIndex, num_rows)
print(
    f'Time to insert {num_rows:,} rows without index: {time_without_index:,} seconds\n'
)

# Insert data into table with index
print(f'Writing Data - {num_rows:,} rows with an index')
time_with_index = insert_data(session, WithIndex, num_rows)
print(f'Time to insert {num_rows:,} rows with index: {time_with_index:,} seconds\n')

diff = calc_time(time_without_index, time_with_index)
print(f'Adding index increased inserting data time by: {diff:.2f}% 😱😱\n\n')


# =============================================================
#                       QUERYING DATA
# =============================================================
print('Reading Data')
num_rows = session.query(WithoutIndex).count()
time_without_index = fetch_data(session, WithoutIndex)
print(f'Time to query {num_rows:,} rows without index: {time_without_index:,} seconds')

num_rows = session.query(WithIndex).count()
time_with_index = fetch_data(session, WithIndex)
print(f'Time to query {num_rows:,} rows with index: {time_with_index:,} seconds')

diff = calc_time(time_without_index, time_with_index)
print(f'Adding index sped up query by: {diff:.2f}% 🎉🎉\n\n')


# =============================================================
#                       CLEAN UP SESSION
# =============================================================
session.close()
 ```


 ```python

from sqlalchemy import create_engine, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///:memory:', echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)

# Add an index programmatically here
user_name_index = Index('ix_users_name', User.name)
user_name_index.create(bind=engine)
user_name_index.drop(bind=engine)
user_name_index.drop(bind=engine, checkfirst=True)

 ```

 ```python
 
from sqlalchemy import Index, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///:memory:', echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)  # Add the index here

    __table_args__ = (
        # The first argument is the index name and the second argument is the column name we want to use
        # here we just put the string representation of the column name
        # Be sure to add a comma to make the __table_args__ a tuple
        Index('ix_users_name', 'name'),
    )


Base.metadata.create_all(engine)
 ```

 ```python

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///:memory:', echo=True)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)  # Add the index here


Base.metadata.create_all(engine)
 ```