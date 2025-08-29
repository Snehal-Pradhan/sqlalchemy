from models import User,engine,Address
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

Address_1 = Address(state = "ABC" , city = "ASNAMD")
user_f = session.query(User).filter(User.id == 1).first()
session.commit()
users = session.query(User).all()
for user in users:
    print(user.addresses[0]) if user.addresses else print(None)

session.close()