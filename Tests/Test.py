from Pylite import Database, Table


def CreateDatabase():
    db = Database()
    db.CreateTable("Users").AddColumn(
        Name = str,
        Age = int,
    )
    db.Users.Insert(Name="John", Age=20)
    db.Save("Database.pylite","password")
    
def CreateFromSQL():
    db = Database()
    db.LoadFromSQL("Database.db")
    db.Save("Database.pylite","password")
    
    

# CreateFromSQL()
db = Database(Path="Database.pylite",Password="password",AutoSave=True)
print(db.Accounts.Select(db.Accounts.ID > 0))