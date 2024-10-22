from src.Pylite import Database


db = Database("DataBase.pylite", "Pass123", True)
db.ExpertExperience.Delete(db.ExpertExperience.ID == 3)
print(db.ExpertExperience)