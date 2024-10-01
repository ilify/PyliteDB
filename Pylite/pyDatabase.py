import Pylite.pyTable as Table


class Database():
    def __init__(self):
        self.Tables = {}
    
    
    def CreateTable(self,TableName) -> Table:
        self.Tables[TableName] = Table()
        self.add_property(TableName)
        return self.Tables[TableName]
    
    def __len__(self) -> int:
        return len(self.Tables.keys())
    
    def add_property(self, name):
        setattr(self.__class__, name, property(lambda self: self.Tables[name]))
    
    