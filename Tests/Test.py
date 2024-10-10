from Pylite import Database,Table,Column


# Database
db = Database("Database","Pylite")
print(db.Users.Select(db.Users.Name.match("J")))
