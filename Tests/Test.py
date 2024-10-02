from Pylite import Database,Table,Column



#Table
t = Table("Users")
t.AddColumn(
    Id = [int,"PrimaryKey","AutoIncrement"],
    Name = str,
    Age = int,
    Salary = float
)
t.RenameColumn("Name","FullName")
t.FullName.Add("John","Doe","Jane","Doe","Alice","Wonderland")
print(t.FullName)


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



