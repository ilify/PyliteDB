from Pylite import Database


def CreateDatabase():
    db = Database()
    db.CreateTable("Users").AddColumn(
        Name = str,
        Age = int,
    )
    db.Users.Insert(Name="John", Age=20)
    db.Save("Database.pylite","password")
    
    
def LoadDatabase():
    db = Database(Path="Database.pylite",Password="password",AutoSave=True)
    print(db.Users)

LoadDatabase()

