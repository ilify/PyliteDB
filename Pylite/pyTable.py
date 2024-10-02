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
        
    def __str__(self) -> str:
        
        def getMaxLength(column) -> int:
            return max([len(str(x)) for x in column.Data])
        
        def formatCell(cell, maxLen):
            return f"{cell}{' '*(maxLen-len(str(cell)))}"
        
        maxLenperColumn = [max(getMaxLength(col), len(key))+self.PrintPadding for col, key in zip(self.Columns.values(), self.Columns.keys())]
        numberOfLines = max([len(col.Data) for col in self.Columns.values()])
        ret = f"Table: {self.TableName}\n"
        ret += "|".join([formatCell(list(self.Columns.keys())[i], maxLenperColumn[i]) for i in range(len(self.Columns))]) + "\n"
        ret += "\n".join("|".join(formatCell(col.Data[i], maxLen) for col, maxLen in zip(self.Columns.values(), maxLenperColumn)) for i in range(numberOfLines)) + "\n"
        
        return ret

    
    