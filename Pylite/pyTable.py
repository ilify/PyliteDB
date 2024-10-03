from .pyColumn import Column
from typing import Optional, Union, Type
class Table:
    def __init__(self, TableName):
        self.TableName:str = TableName
        self.Columns: dict[str, Column] = {}
        self.PrintPadding = 1

    def __getitem__(self, Key) -> Column:
        return self.Columns[Key]

    def __getattr__(self, name: str) -> Optional[Column]:
        if name in self.Columns:
            return self.Columns[name]
        raise AttributeError(f"Column '{name}' not found.")
    

    def AddColumn(self,**columns: Union[list, Type]):
        for ColumnName, ColumnData in columns.items():
            if isinstance(ColumnData, list):
                self.Columns[ColumnName] = Column(ColumnData[0], ColumnData[1:])
            elif isinstance(ColumnData, type):
                self.Columns[ColumnName] = Column(ColumnData, [])
            setattr(self.__class__, ColumnName, property(lambda self, name=ColumnName: self.Columns[name]))

    def RenameColumn(self, OldName, NewName):
        self.Columns[NewName] = self.Columns.pop(OldName)
        setattr(self.__class__, NewName, property(lambda self, name=NewName: self.Columns[name]))
        delattr(self.__class__, OldName)
        
    def RemoveColumn(self, ColumnName):
        del self.Columns[ColumnName]
        delattr(self.__class__, ColumnName)
        
    def Insert(self, **columns: Union[list, Type]):
        for k,v in self.Columns.items():
            if k in list(columns.keys()):
                if "Unique" in v.Options and columns[k] in v.Data:
                    raise ValueError(f"Value '{columns[k]}' already exists in '{k}' column with Unique Option.")
                v.Add(v.Type(columns[k]))
            else:
                if "AutoIncrement" in v.Options:
                    v.Add(v.Type(max(v.Data)+1))
                else:
                    v.Add(v.Type())
    
    def Select(self, what,where=None):
        ReturnTable = Table("Selected Table")
        if what == None and where == None:
            [ReturnTable.AddColumn(**{c: self.Columns[c].Type}) for c in self.Columns.keys()]
            [v.Add(*self.Columns[k].Data) for k,v in ReturnTable.Columns.items()]
        
        if where == None:
            [ReturnTable.AddColumn(**{c: self.Columns[c].Type}) for c in what]
            [v.Add(*self.Columns[k].Data) for k,v in ReturnTable.Columns.items()]
            
        if where != None:
            [ReturnTable.AddColumn(**{c: self.Columns[c].Type}) for c in what]
            [ReturnTable.Columns[i].Add(*[self.Columns[i].Data[j] for j in range(len(where)) if where[j]]) for i in ReturnTable.Columns]
                        
        return ReturnTable

    def Delete(self,index=None,where=None):
        if self.isEmpty():raise ValueError("Table is empty.")
        if index == None and where == None:
            self.Columns = {k: Column(v.Type, v.Options) for k,v in self.Columns.items()}
        if index != None:
            [v.RemoveAt(index) for v in self.Columns.values()]
        if where != None:
            [x.RemoveByList(where) for x in self.Columns.values()]
            

    def Update(self, index=None, where=None, **columns: Union[list, Type]):
        if index == None and where == None:
            raise ValueError("Please provide either index or where condition.")
        if index != None:
            for k,v in columns.items():
                self.Columns[k].Data[index] = v
        if where != None:
            for k,v in columns.items():
                for i in range(len(where)):
                    if where[i]:
                        self.Columns[k].Data[i] = v

    def isEmpty(self) -> bool:
        return all([col.isEmpty() for col in self.Columns.values()])
    
    def __str__(self) -> str:
        if self.isEmpty():return f"Table: {self.TableName} is empty."
        def getMaxLength(column) -> int:return max([len(str(x)) for x in column.Data])
        def formatCell(cell, maxLen):return f" {cell} {' '*(maxLen-len(str(cell)))}"
        maxLenperColumn = [max(getMaxLength(col), len(key))+self.PrintPadding for col, key in zip(self.Columns.values(), self.Columns.keys())]
        numberOfLines = max([len(col.Data) for col in self.Columns.values()])
        ret = f"Table: {self.TableName}\n"
        ret += "| "+"|".join([formatCell(list(self.Columns.keys())[i], maxLenperColumn[i]) for i in range(len(self.Columns))]) + " |\n"
        ret +=  "| "+" |\n| ".join("|".join(formatCell(col.Data[i], maxLen) for col, maxLen in zip(self.Columns.values(), maxLenperColumn)) for i in range(numberOfLines)) + " |"
        return ret

    
    