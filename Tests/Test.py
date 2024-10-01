from Pylite import Database,Table,Column

#Column
c = Column(int)
c.AddAll(10,20,30,40,50,65640,0,80,90,100,110,120,130,140,150000)
c[c.between(10,100)] = -1
c.Removeif(lambda x: x == -1)
c.Apply(lambda x: x ** 2)
print(c)

#Create Table
# db.CreateTable("Users").AddColumns(
#     name=str,
#     age=int,
#     email=str
# )

#Insert
# db.Users.Insert(
#     name="John20",
#     age=20,
#     email="test@example.com"
# )
# db.Users.Insert(
#     name="John25",
#     age=25,
#     email="test@example.com"
# )
# db.Users.Insert(
#     name="John35",
#     age=35,
#     email="test@example.com"
# )

#Read All
# print(db.Users)

#Read Specific
# print(db.Users[db.Users.age.between(20,30)])
# print(db.Users[(db.Users.age >= 20) & (db.Users.age <= 30)])

#Delete
# db.Users.Delete(db.Users.age.between(20,30))

#Update
# db.Users.age.apply(lambda x: x+1)

# print(db.Users)
