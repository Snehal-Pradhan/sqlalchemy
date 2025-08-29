### Query Options
- Optimize your queries
- Eager Query Options

```python

from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

db_url = 'sqlite:///ep_13_options_eager_loading.db'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    posts: Mapped[list['Post']] = relationship(
        backref='user',
        lazy='select',
    )

    def __repr__(self):
        return f'<User {self.name} >'


class Post(Base):
    __tablename__ = 'posts'
    active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    detail: Mapped['Detail'] = relationship(backref='post', lazy='select')

    @classmethod
    def is_active(cls):
        return cls.active is True

    def __repr__(self):
        return f'<Post {self.id} >'


class Detail(Base):
    __tablename__ = 'details'
    content: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Detail {self.id} - content: {self.content}>'


# Create the database tables
Base.metadata.create_all(engine)

if __name__ == '__main__':
    user_1 = User(name='Zeq')
    user_1.posts = [
        Post(detail=Detail(content='This is an example post detail')),
        Post(detail=Detail(content='Subscribe to Zeq Tech!'), active=True),
    ]

    user_2 = User(name='Bill')
    user_2.posts = [
        Post(detail=Detail(content='This is another example of some post details')),
        Post(detail=Detail(content='Yes!')),
    ]

    session.add_all([user_1, user_2])
    session.commit()
```


```python

from sqlalchemy import select
from sqlalchemy.orm import (
    contains_eager,
    defaultload,
    immediateload,
    joinedload,
    load_only,
    selectinload,
    subqueryload,
)

from models import Detail, Post, User, session


# Loading Options:
# defaultload()         - when you dont want to change the loading behavior but you
#                         want to change something in the loaded items from the relationship

# Eager loading: (Loaded right away)
# joinedload()          - load related data with a join statement
# subqueryload()        - loads data using a subquery
# immediateload()       - loads everything in the relationship one by one, can add a recursion depth for self relationships
#                         ex: followers / following relationships
# selectinload()        - more efficient than `immediateload`,` creating one select statment for all related objects

# Special:
# contains_eager()  - allows filtering on related items

# =============================================================================================
# Default Loading
print('=' * 40)
print('\nLoading from class structure')
query = session.query(User)
print(query)

print('=' * 40)
print('\nLoading with the: `defaultload` function')
query = session.query(User).options(defaultload(User.posts))
print(query)

# =============================================================================================
# Eager Loading

print('=' * 40)
print('\nLoading with the: `joinedload` function')
query = session.query(User).options(joinedload(User.posts))
print(query)
print(query.all())

print('=' * 40)
print('\nLoading with the: `subqueryload` function')
query = session.query(User).options(subqueryload(User.posts))
print(query)
print(query.all())

print('=' * 40)
print('\nLoading with the: `immediateload` function')
query = session.query(User).options(immediateload(User.posts))
print(query)
print(query.all())

print('=' * 40)
print('\nLoading with the: `selectinload` function')
query = session.query(User).options(selectinload(User.posts))
print(query)
print(query.all())

# =============================================================================================
# Select use of joinedload and contains_eager
print('=' * 40)
print('\nLoading with the: `joinedload` function')
query = (
    select(User).options(joinedload(User.posts)).filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(session.execute(query).unique().all())

print('=' * 40)
print('\nLoading with the: `contains_eager` function')
query = (
    select(User)
    .outerjoin(Post)
    .options(contains_eager(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(session.execute(query).unique().all())

# Query use of joinedload and contains_eager
print('=' * 40)
print('\nLoading with the: `joinedload` function')
query = (
    session.query(User)
    .options(joinedload(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(query.all())

# contains eager requires us to specify a join condition,
# but also allows us to filter onthe joined data
print('=' * 40)
print('\nLoading with the: `contains_eager` function')
query = (
    session.query(User)
    .outerjoin(Post)
    .options(contains_eager(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
)
print(query)
print(query.all())

# =============================================================================================
# Calling .options() allows to add more query options to relationship data
print('=' * 40)
print('\nMore `.options()` loading')
print('\nApply `load_only()` to only load selected columns')
query = (
    session.query(User)
    .outerjoin(Post)
    .options(
        contains_eager(User.posts).options(joinedload(Post.detail), load_only(Post.id))
    )
)
print(query)

print('=' * 40)
print('\nMore `.options()` loading')
query = session.query(User).options(
    joinedload(User.posts).options(joinedload(Post.detail), load_only(Post.id))
)
print(query)

# Calling .options() allows to add more query options to relationship data
print('=' * 40)
print('\nLoad only the Post id for all Posts for a User')
query = session.query(User).options(joinedload(User.posts).load_only(Post.id))
print(query)

print('=' * 40)
print("\nLoad all Posts for User and only the Detail's content for each post")
query = session.query(User).options(
    joinedload(User.posts).joinedload(Post.detail).load_only(Detail.content)
)
print(query)

# =============================================================================================
# Multiple loadings
print('=' * 40)
print('\nSub Relationship loading')
query = session.query(User).options(selectinload(User.posts).options(joinedload(Post.detail)))
print(query)
print(query.all())

print('=' * 40)
print('\nMultiple relationship loading')
query = session.query(User).options(
    selectinload(User.posts),
    # joinedload(User.<some other relationship on the user table>)
)
print(query)
print(query.all())
```

- Lazy Query Options
```python 

from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from datetime import datetime

db_url = 'sqlite:///ep_14_options_lazy_load.db'

engine = create_engine(db_url, echo=True)

Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    status: Mapped[str | None]
    posts: Mapped[list['Post']] = relationship(
        backref='user',
        lazy='select',
    )
    preference: Mapped['Preference'] = relationship(
        backref='user',
        lazy='joined',
    )

    def __repr__(self):
        return f'<User {self.name} >'

class Preference(Base):
    __tablename__ = 'preferences'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    dark_mode: Mapped[bool] = mapped_column(default=False)
    speed: Mapped[float] = mapped_column(default=1.0)

    def __repr__(self):
        return f'<Preferences {self.id} >'

class Post(Base):
    __tablename__ = 'posts'
    active: Mapped[bool] = mapped_column(default=True)
    date: Mapped[datetime] = mapped_column(default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    detail: Mapped['Detail'] = relationship(backref='post', lazy='select')

    def __repr__(self):
        return f'<Post {self.id} >'


class Detail(Base):
    __tablename__ = 'details'
    content: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Detail {self.id} - content: {self.content}>'


# Create the database tables
Base.metadata.create_all(engine)

if __name__ == '__main__':
    user_1 = User(name='Zeq', preference=Preference(dark_mode=True, speed=2.5))
    user_1.posts = [
        Post(detail=Detail(content='This is an example post detail')),
        Post(detail=Detail(content='Subscribe to Zeq Tech!'), active=True),
    ]

    user_2 = User(name='Bill', preference=Preference())
    user_2.posts = [
        Post(detail=Detail(content='This is another example of some post details')),
        Post(detail=Detail(content='Yes!')),
    ]

    session.add_all([user_1, user_2])
    session.commit()
```

```python

from sqlalchemy import select
from sqlalchemy.orm import (
    contains_eager,
    joinedload,
    lazyload,
    load_only,
    noload,
    raiseload,
)

from models import Detail, Post, User, session

# Loading Options:

# Lazy Loading (Loaded maybe when accessed)
# noload()          - doesn't load the data at all
# lazyload()        - will load the data only when accessed
# raiseload()       - doesn't load the data - will raise an error if the data is accessed

# Special:
# load_only()       - only load specific columns

# =============================================================================================
# Lazy Loading

print('=' * 40)
print('\nLoading with the: `noload` function')
query = session.query(User).options(noload(User.posts))
print(query)
print(query.all())


print('=' * 40)
print('\nLoading with the: `lazyload` function')
query = session.query(User).options(lazyload(User.posts))
print(query)
print(query.all())


print('=' * 40)
print('\nLoading with the: `raiseload` function')
query = session.query(User).options(raiseload(User.posts))
print(query)
print(query.all())

# =============================================================================================
# Calling .options() allows to add more query options to relationship data
print('=' * 40)
print('\nMore `.options()` loading')
print('\nApply `load_only()` to only load selected columns')
query = (
    session.query(User)
    .outerjoin(Post)
    .options(
        contains_eager(User.posts).options(joinedload(Post.detail), load_only(Post.id))
    )
)
print(query)

print('=' * 40)
print('\nMore `.options()` loading')
query = session.query(User).options(
    joinedload(User.posts).options(joinedload(Post.detail), load_only(Post.id))
)
print(query)

# Calling .options() allows to add more query options to relationship data
print('=' * 40)
print('\nLoad only the Post id for all Posts for a User')
query = session.query(User).options(joinedload(User.posts).load_only(Post.id))
print(query)

print('=' * 40)
print("\nLoad all Posts for User and only the Detail's content for each post")
query = session.query(User).options(
    joinedload(User.posts).joinedload(Post.detail).load_only(Detail.content)
)
print(query)

# =============================================================================================
# load_only()
print('=' * 40)
print('\nUsing the: `load_only` function in options')
print('\nApply `load_only()` to only load selected columns')
query = select(User).options(joinedload(User.posts).options(load_only(Post.active)))
print(query)

# Need to add unique when adding a joinedload or
# contains_eager when using `select()`
print(session.scalars(query).unique().all())

# =============================================================================================
# Multiple Loading

print('=' * 40)
print('\nJoin load the posts, lazily load the preferences')
query = (
    session.query(User)
    .options(
        joinedload(User.posts),
        lazyload(User.preference)
    )
)
print(query)
print(query.all())

# =============================================================================================
# Chained Loading

print('=' * 40)
print('\nApply CHained loading')
query = (
    session.query(User)
    .options(
        joinedload(User.posts)
        .lazyload(Post.detail)
    )
)
print(query)
print(query.all())
```