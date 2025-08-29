### Cascades

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'))
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


session = SessionLocal()

```

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade="save-update, merge"
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'))
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


session = SessionLocal()

```
```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()

print(session.query(Child).all()) 

parent.children.clear()
session.commit()

print(session.query(Child).all()) 
```

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='save-update, delete'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()

print(session.query(Child).all())  # Not Empty

session.delete(parent)
session.commit()

print(session.query(Child).all())  # Empty


```

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm.exc import DetachedInstanceError


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='save-update, expunge'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(
        back_populates='children', cascade='expunge'
    )

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()

session.expunge(parent)

assert parent not in session
# try:
print(parent.children[0])
# except DetachedInstanceError:
#     print('parent.children are not in the session')
```

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey
from typing import List


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = 'parents'
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List['Child']] = relationship(
        back_populates='parent', cascade='save-update, merge'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child id: {self.id} parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Create and commit parent and child
session = SessionLocal()
parent = Parent(children=[Child()])
session.add(parent)
session.commit()
print(f"Original committed parent: {parent}")
session.close()

# Since the session was closed, the parent is now detatched.
# Add a new child while detached
parent.children.append(Child())

# Merge back into a new session
session = SessionLocal()
merged = session.merge(parent)  # Merges the updated object
print(f"Merged parent in session: {merged}")
session.commit()

# Query to confirm children were merged
fetched = session.query(Parent).first()
print(f"Fetched from DB: {fetched}")
session.close()

```

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey
from typing import List


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = 'parents'
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List['Child']] = relationship(
        back_populates='parent', cascade='save-update, merge'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child id: {self.id} parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Create and commit parent and child
session = SessionLocal()
parent = Parent(children=[Child()])
session.add(parent)
session.commit()
print(f"Original committed parent: {parent}")
session.close()

# Since the session was closed, the parent is now detatched.
# Add a new child while detached
parent.children.append(Child())

# Merge back into a new session
session = SessionLocal()
merged = session.merge(parent)  # Merges the updated object
print(f"Merged parent in session: {merged}")
session.commit()

# Query to confirm children were merged
fetched = session.query(Parent).first()
print(f"Fetched from DB: {fetched}")
session.close()

```
```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='save-update, refresh-expire'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'), nullable=True)
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

parent = Parent(children=[Child()])
session.add(parent)
session.commit()

print("\nBefore Expire:")
print(parent.children) 
print(parent.children) 
session.expire(parent)
# session.expire_all([parent])

# Re-fetches from DB if accessed
print("\nAfter Expire:")
print(parent.children) 

```

```python
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy import create_engine, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Parent(Base):
    __tablename__ = 'parents'
    children: Mapped[list['Child']] = relationship(
        back_populates='parent', cascade='save-update'
    )

    def __repr__(self):
        return f'<Parent id: {self.id} children: {self.children}>'


class Child(Base):
    __tablename__ = 'children'
    parent_id: Mapped[int] = mapped_column(ForeignKey('parents.id'))
    parent: Mapped['Parent'] = relationship(back_populates='children')

    def __repr__(self):
        return f'<Child - parent_id: {self.parent_id}>'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


session = SessionLocal()

parent = Parent()
child = Child()
parent.children.append(child)

# Only add the parent to session
session.add(parent)

# Child is automatically added
assert child in session

print('Before committing')
print(parent)
print(child)
session.commit()

print('\nAfter committing')
print(parent)
print(child)

```