from Pylite import Database,Table,Column


# Database
db = Database()
db.CreateTable("Users")
db.Users.AddColumn(ID=int,Unique=True)
db.Users.AddColumn(Name=str)
db.Users.AddColumn(Age=int)
db.Users.Insert(ID=1,Name="John",Age=25)
db.Users.Insert(ID=2,Name="Jane",Age=30)
db.Users.Insert(ID=3,Name="Jack",Age=35)
print(db.Users.Select(db.Users.Age > 30))