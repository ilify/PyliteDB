import json
from .Column import Column
from typing import Optional, Union, Type, Callable

class Table:
    PrintPadding = 1
    def __init__(self, TableName,SaveCallback=None):
        self.Columns: dict[str, Column] = {}
        self.TableName = TableName
        self.Save = SaveCallback

    def __getitem__(self, Key) -> Column:
        return self.Columns[Key]

    def __getattr__(self, name: str) -> Optional[Column]:
        if name in self.Columns:
            return self.Columns[name]
        raise AttributeError(f"Column '{name}' not found.")

    def AddColumn(self, **columns: Union[list, Type]):
        for ColumnName, ColumnData in columns.items():
            if isinstance(ColumnData, list):
                self.Columns[ColumnName] = Column(ColumnData[0], ColumnData[1:], self.Save)
            elif isinstance(ColumnData, type):
                self.Columns[ColumnName] = Column(ColumnData, [], self.Save)
            setattr(self.__class__, ColumnName, property(lambda self, name=ColumnName: self.Columns[name]))
        self.Save()

    def RenameColumn(self, OldName, NewName):
        self.Columns[NewName] = self.Columns.pop(OldName)
        setattr(self.__class__, NewName, property(lambda self, name=NewName: self.Columns[name]))
        delattr(self.__class__, OldName)
        self.Save()
        
    def RemoveColumn(self, ColumnName):
        del self.Columns[ColumnName]
        delattr(self.__class__, ColumnName)
        self.Save()
        
        
    def Insert(self, **columns: Union[list, Type]):
        for k,v in self.Columns.items():
            if k in list(columns.keys()):
                v.Add(v.Type(columns[k]))
            else:
                v.Add(v.Type())
        self.Save()

    # @NotImplemented    
    # def InsertObject(self,obj):
    #     print(obj.__dict__)
    #     try:
    #         for k,v in self.Columns.items():
    #             if k in obj.__dict__.keys():
    #                 v.Add(v.Type(obj.__dict__[k]))
    #             else:
    #                 v.Add(v.Type())
    #     except Exception as e:
    #         print(f"Error: {e}")    
    #     self.Save()

            
                
    
    def Select(self,condition):
        ReturnTable = Table("Selected Table")
        ReturnTable.Columns = {k: Column(v.Type, v.Options) for k,v in self.Columns.items()}
        for i in range(self.RowCount):
            if condition[i]:
                ReturnTable.Insert(**{k:self.Rows[i][j] for j,k in enumerate(self.Columns.keys())})
        return ReturnTable

    def Delete(self,index=None,where=None):
        if self.isEmpty():raise ValueError("Table is empty.")
        if index == None and where == None:
            self.Columns = {k: Column(v.Type, v.Options) for k,v in self.Columns.items()}
        if index != None:
            [v.RemoveAt(index) for v in self.Columns.values()]
        if where != None:
            [x.RemoveByList(where) for x in self.Columns.values()]
        self.Save()
        

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
        self.Save()

        

    def isEmpty(self) -> bool:
        return all([col.isEmpty() for col in self.Columns.values()])
    
    def __str__(self) -> str:
        if self.isEmpty():return f"Table is empty."
        def getMaxLength(column) -> int:return max([len(str(x)) for x in column.Data])
        def formatCell(cell, maxLen):return f" {cell} {' '*(maxLen-len(str(cell)))}"
        maxLenperColumn = [max(getMaxLength(col), len(key))+self.PrintPadding for col, key in zip(self.Columns.values(), self.Columns.keys())]
        numberOfLines = max([len(col.Data) for col in self.Columns.values()])
        ret = f"{self.TableName}:\n"
        ret += "| "+"|".join([formatCell(list(self.Columns.keys())[i], maxLenperColumn[i]) for i in range(len(self.Columns))]) + " |\n"
        ret +=  "| "+" |\n| ".join("|".join((formatCell(col.Data[i], maxLen) if col.Type!=bytes else "BLOB") for col, maxLen in zip(self.Columns.values(), maxLenperColumn)) for i in range(numberOfLines)) + " |"
        return ret
    
    @property
    def Rows(self) -> list:
        return [[col.Data[i] for col in self.Columns.values()] for i in range(len(self.Columns[list(self.Columns.keys())[0]].Data))]
    
    def GetColumns(self) -> list:
        return list(self.Columns.keys())
    
    def Exists(self, **columns: Union[list, Type]) -> bool:
        for k,v in columns.items():
            if k not in self.Columns.keys():return False
            if v not in self.Columns[k].Data:return False
        return True
    
    @property
    def RowCount(self) -> int:
        return len(self.Rows)
    
    
    
    def toJson(self):
        return {"Columns":{k:v.toJson() for k,v in self.Columns.items()}}