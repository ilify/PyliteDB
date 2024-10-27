from src.Pylite import Database

# db = Database.LoadFromSQL("DataBase.db").Save("DataBase.pylite","password")
db = Database("DataBase.pylite","password")

db.Link(
    source = db.Experts.ID,
    targets = [db.ExpertExperience.ID,db.Reviews.ExpertID]
)

db.Experts.DeleteAt(0)
print(db.ExpertExperience)
# print(db.)

