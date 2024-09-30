from Pylite import Database

#Create Database
db = Database()

#Create Table
db.CreateTable("Users").AddColumns(
    name=str,
    age=int,
    email=str
)

#Insert
db.Users.Insert(
    name="John20",
    age=20,
    email="test@example.com"
)
db.Users.Insert(
    name="John25",
    age=25,
    email="test@example.com"
)
db.Users.Insert(
    name="John35",
    age=35,
    email="test@example.com"
)

#Read All
print(db.Users)

#Read Specific
print(db.Users[db.Users.age.between(20,30)])
print(db.Users[(db.Users.age >= 20) & (db.Users.age <= 30)])

#Delete
db.Users.Delete(db.Users.age.between(20,30))

#Update
# db.Users.Update(db.Users.age.between(20,30),25)
