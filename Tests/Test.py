from Pylite import Database,Table,Column

#Column
c = Column(int)
#Insert
c.Add(50,60,70,80,90,100)

#Select
c.Get(0)
c.GetIf(lambda x: x > 50)

#Delete
c.RemoveFirst()
c.RemoveLast()
c.RemoveAll(70)
c.RemoveAt(1)
c.RemoveIf(lambda x: x > 80)

#Update
c.Apply(lambda x: x + 10)
c.ApplyIf(lambda x: 80,lambda x: x > 100)




