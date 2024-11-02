from src.Pylite import Database,email,password,Table

db = Database("DataBase.pylite", "password",AutoSave=True)#.LoadFromSQL("test.db")
# db.Users.afterInsert = lambda table,added: print("Inserted",added)
# db.Users.Insert(ID = 1, Email = "ilies@gmail.com", Password = "passwordA1.")
print(db.Users[0])



# db = Database()
# db.CreateTable("Users").AddColumn(
#     ID = int,
#     Email = email,
#     Password = password
# )
# db.Users.afterInsert = lambda table,added: print("Inserted",added.Email)
# db.Save("DataBase.pylite", "password")
