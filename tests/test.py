from src.Pylite import Database


def CreateDatabase():
    db = Database()
    db.CreateTable("Users").AddColumn(
        ID=int, Name=str, Age=int, Email=str, Password=str
    )
    db.Users.beforeInsert = lambda self: print(self)
    db.Users.afterInsert = lambda self: print(self)
    db.Users.Insert(
        ID=1, Name="Ilify", Age=20, Email="ilies@gmail.com", Password="1234"
    )


CreateDatabase()
