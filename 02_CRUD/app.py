from models import engine,User
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

User_1 = User(name="Steve",age=24)
User_2 = User(name="John",age=73)
User_3 = User(name="Jane",age=49)
User_4 = User(name="Marshal",age=19)

session.add_all([User_1,User_2,User_3,User_4])
session.commit()
