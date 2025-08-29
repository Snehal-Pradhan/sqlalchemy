### Events 
```python

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, Mapper
from sqlalchemy.engine import Connection

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


user = User(name='User 1', email='user_1@example.com')
session.add(user)
session.commit()


# Add an event through a decorator
@event.listens_for(User, 'before_update')
def audit_user_update(mapper: Mapper, connection: Connection, target: User):
    stmt = text('SELECT email FROM users WHERE id = :user_id')
    old_email = connection.scalar(stmt, {'user_id': target.id})
    new_email = target.email
    if new_email != old_email:
        print(f'Email changed for user {target.id}: {old_email} -> {new_email}')


user = session.query(User).filter_by(name='User 1').first()
user.email = 'user_updated@example.com'
session.commit()
```

```python

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, Mapper
from sqlalchemy.engine import Connection

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def insert_user_listener(mapper: Mapper, connection: Connection, target: User):
    print(f'[EVENT: before_insert ] Inserting user: {target.name}')


# Add an event through a function call
event.listen(User, 'before_insert', insert_user_listener)

for x in range(1, 10):
    user = User(name=f'User {x}', email=f'user_{x}@email.com')
    session.add(user)

session.commit()

```

```python

from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


# Define a simple User model
class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Event Listener Functions
def log_event(name):
    """Decorator to log SQLAlchemy events"""

    def wrapper(*args, **kwargs):
        print(f'🔹 {name} triggered!')

    return wrapper


# Session Lifecycle Events
event.listen(Session, 'before_flush', log_event('before_flush'))
event.listen(Session, 'after_flush', log_event('after_flush'))
event.listen(Session, 'after_flush_postexec', log_event('after_flush_postexec'))
event.listen(Session, 'before_commit', log_event('before_commit'))
event.listen(Session, 'after_commit', log_event('after_commit'))
event.listen(Session, 'after_rollback', log_event('after_rollback'))

#  Object Lifecycle (Mapper) Events
event.listen(User, 'before_insert', log_event('before_insert'))
event.listen(User, 'after_insert', log_event('after_insert'))
event.listen(User, 'before_update', log_event('before_update'))
event.listen(User, 'after_update', log_event('after_update'))
event.listen(User, 'before_delete', log_event('before_delete'))
event.listen(User, 'after_delete', log_event('after_delete'))

# Execution Events
event.listen(engine, 'before_execute', log_event('before_execute'))
event.listen(engine, 'after_execute', log_event('after_execute'))

# Transaction Test Cases
try:
    print('\nINSERT OPERATION')
    user = User(name='Zeq')
    session.add(user)
    session.flush()
    session.commit()

    print('\nQuery OPERATION')
    u = session.query(User).all()
    print('\nQuery OPERATION')
    u = session.execute(select(User)).all()
    print('\nQuery OPERATION')
    u = session.scalar(select(User))

    print('\nUPDATE OPERATION')
    user.name = 'Zeq Updated'
    session.flush()
    session.commit()

    print('\nUPDATE OPERATION')
    user.name = 'Zeq Updated'
    session.flush()

    print('\nDELETE OPERATION')
    session.delete(user)
    session.flush()
    session.commit()

    print('\nROLLBACK OPERATION')
    user1 = User(name='Zeq')
    session.add(user1)

    user2 = User(name='Zeq')  # 🚨 Violates UNIQUE constraint
    session.add(user2)
    session.commit()  # This will fail!

except Exception as e:
    print(f'❌ Error: {e}')
    session.rollback()

```

```python

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase, Mapper
from sqlalchemy.engine import Connection
import re

engine = create_engine('sqlite:///:memory:')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class BlogPost(Base):
    __tablename__ = 'blog_posts'
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Add an event through a decorator
@event.listens_for(BlogPost, 'before_insert')
def generate_slug(mapper: Mapper, connection: Connection, target: BlogPost):
    if target.title:
        slug = re.sub(r'[^\w]+', '-', target.title.lower())
        target.slug = slug


# Add an event through a function call
event.listen(BlogPost, 'before_update', generate_slug)

post = BlogPost(title='Decorators are super cool')
session.add(post)
session.commit()

print(post.slug)

post.title = 'Subscribe to Zeq Tech'
session.commit()
print(post.slug)
```