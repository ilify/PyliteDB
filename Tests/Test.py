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
Accounts : Table = db.Accounts
# Accounts.Delete(Accounts.RowCount-1)
print(Accounts.Select(Accounts.Email.match(".*@gmail.com")))

