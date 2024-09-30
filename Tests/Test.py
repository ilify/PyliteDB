from Pylite import Database


db = Database()

db.CreateTable("Users").AddColumns(
    name=str,
    age=int,
    email=str
)

Users = db["Users"]

Users.Insert(
    name="John20",
    age=20,
    email="test@example.com"
)
Users.Insert(
    name="John25",
    age=25,
    email="test@example.com"
)
Users.Insert(
    name="John35",
    age=35,
    email="test@example.com"
)

print(Users[Users["age"] > 32]) #  John35 35  test@example.com
