from Pylite.pyColumn import Column
class Table():
    def __init__(self,TableName):
        self.TableName = TableName
        self.Columns : dict = {}
    
    def AddColumn(self,name,Type):
        self.Columns[name] = Column(Type)
        
    
    def AddColumns(self,**Columns):
        pass
    
    def Insert(self,**Data):
        pass
        
        
    def Delete(self,Condition):
        pass
    
    
    def Update(self,func):
        pass
    
    def Get(self,Key):
        pass