from Pylite import Database,Table,Column

#Column
c = Column(int)
#Insert
c.Add(50,60,70,80,90,100,110,120,130,140,150)

#Select
c.Get(0) #Read Only
c.GetIf(lambda x: x > 50) #Read Only

#Delete
c.RemoveFirst()
c.RemoveLast()
c.RemoveAll(70)
c.RemoveAt(1)
c.RemoveIf(lambda x: x < 80)

#Update
c.ApplyIf(lambda x: x**2,lambda x: x > 100)


c.ReType(float)
print(c)



