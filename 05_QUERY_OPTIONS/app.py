
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


query=session.query(User)
print(query)

query=session.query(User).options(subqueryload(User.posts))
print(query)