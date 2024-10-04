from Pylite import Database,Table,Column


# Database
db = Database("db.pylite",key="password")
# db.CreateTable("Users")
# db.Users.AddColumn(
#     Name = str,
#     Age = int
    
# )

# db.Users.Insert(Name = "John", Age = 20)
print(db.Users)
# db.Save("db.pylite")