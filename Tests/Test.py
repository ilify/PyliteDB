from Pylite import Database,Table,Column



#Table
t = Table("Users")
t.AddColumn(
    Id = [int,"AutoIncrement","Unique"],
    Name = str,
    Age = int,
    Salary = float
)
t.Id.Add(1,2,3,4,5,6,7,8,9,10)
t.Name.Add("John","Jane","Jim","Jack","Jill","Joe","Jenny","Jerry","Jesse","Jade")
t.Age.Add(25,22,30,35,40,45,50,55,60,65)
t.Salary.Add(50000.0,45000.0,55000.0,60000.0,65000.0,70000.0,75000.0,80000.0,85000.0,90000.0)



t.Insert(
    Name="John",
    Age=25,
    Salary=50000
)
t.Insert(
    Name="John",
    Age=25,
    Salary=50000
)

print(t)

# t.Select(
#     ["Name","Age"], # if all data is needed, pass Nothing Select(where=t.Age > 20)
#     where = t.Age > 20
# )

# t.Delete(0) #index
# t.Delete(where=t.Age < 20) #condition

# t.Update(
#     0,  # index of the row
#     Name="Jane",  # fields to update
#     Age=30
# )

# t.Update(
#     where=t.Age < 25,  # condition to find rows
#     Salary=55000.0  # fields to update
# )

# t.Update(
#     where = t.Id == 1,  # condition to find rows
#     Salary=55000.0,  # fields to update
#     Age=60
# )


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



