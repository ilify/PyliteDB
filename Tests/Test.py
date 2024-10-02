from Pylite import Database,Table,Column



#Table
t = Table("Users")
t.AddColumn(
    Id = [int,"PrimaryKey","AutoIncrement"],
    Name = str,
    Age = int,
    Salary = float
)
t.Insert(
    Id=1,
    Name="John",
    Age=25,
    Salary=50000.0
)


t.Select(
    ["Name","Age"], # if all data is needed, pass Nothing Select(where=lambda row: row.Age > 20)
    where=lambda row: row.Age > 20
)

t.Delete(0) #index
t.Delete(where=lambda row: row.Age < 20) #condition

t.Update(
    0,  # index of the row
    Name="Jane",  # fields to update
    Age=30
)

t.Update(
    where=lambda row: row.Age < 25,  # condition to find rows
    Salary=55000.0  # fields to update
)

t.Update(
    where=lambda row: row.Id == 1,  # condition to find rows
    Salary=55000.0,  # fields to update
    Age=60
)


#Column
# c = Column(int)
# #Insert
# c.Add(50,60,70,80,90,100,110,120,130,140,150)

# #Select
# c.Get(0) #Read Only
# c.GetIf(lambda x: x > 50) #Read Only

# #Delete
# c.RemoveFirst()
# c.RemoveLast()
# c.RemoveAll(70)
# c.RemoveAt(1)
# c.RemoveIf(lambda x: x < 80)

# #Update
# c.ApplyIf(lambda x: x**2,lambda x: x > 100)


# c.ReType(float)
# print(c)



