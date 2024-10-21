from src.Pylite import Database


db = Database("DataBase.pylite", "Pass123")
print(db.Meetings.Select(db.Meetings.ID % 2 != 0))
