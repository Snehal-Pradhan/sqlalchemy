from models import session,User

user1 = User(username="Somu")
user2 = User(username="Snehal")
user3 = User(username="Trump")

user1.following.append(user2)
user2.following.append(user3)
user3.following.append(user1)

session.add_all([user1,user2,user3])

session.commit()