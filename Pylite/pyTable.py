from Pylite.pyColumn import Column
class Table():
    def __init__(self,TableName):
        self.TableName = TableName
        self.Columns : dict = {}
    
    