from models import session,User

user1 = User(username="A")
user2 = User(username="B")
user3 = User(username="C")

user1.following.append(user2)
user2.following.append(user3)
user3.following.append(user1)

session.add_all([user1,user2,user3])
session.commit()

print(f"{user1.following = }")
print(f"{user2.following = }")
print(f"{user3.following = }")
session.close()