import json
from .pyColumn import Column
from typing import Optional, Union, Type
class Table:
    PrintPadding = 1
    def __init__(self, TableName):
        self.Columns: dict[str, Column] = {}

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
                    try:
                        v.Add(v.Type(max(v.Data)+1))
                    except:
                        v.Add(v.Type())
                else:
                    v.Add(v.Type())
    
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
        if self.isEmpty():return f"Table is empty."
        def getMaxLength(column) -> int:return max([len(str(x)) for x in column.Data])
        def formatCell(cell, maxLen):return f" {cell} {' '*(maxLen-len(str(cell)))}"
        maxLenperColumn = [max(getMaxLength(col), len(key))+self.PrintPadding for col, key in zip(self.Columns.values(), self.Columns.keys())]
        numberOfLines = max([len(col.Data) for col in self.Columns.values()])
        ret = f"Table:\n"
        ret += "| "+"|".join([formatCell(list(self.Columns.keys())[i], maxLenperColumn[i]) for i in range(len(self.Columns))]) + " |\n"
        ret +=  "| "+" |\n| ".join("|".join(formatCell(col.Data[i], maxLen) for col, maxLen in zip(self.Columns.values(), maxLenperColumn)) for i in range(numberOfLines)) + " |"
        return ret
    
    @property
    def Rows(self) -> list:
        return [[col.Data[i] for col in self.Columns.values()] for i in range(len(self.Columns[list(self.Columns.keys())[0]].Data))]
    
    def Exists(self, **columns: Union[list, Type]) -> bool:
        for k,v in columns.items():
            if k not in self.Columns.keys():return False
            if v not in self.Columns[k].Data:return False
        return True
    
    @property
    def RowCount(self) -> int:
        return len(self.Rows)
    
    def serialize(self) -> str:
        """
        Serializes the Table object to a JSON string.
        """
        return json.dumps({
            "Columns": {k:{
                    "type": v.Type.__name__,
                    "data": v.Data,
                    "options": v.Options
                } for k,v in self.Columns.items()}
        })
    @staticmethod
    def deserialize(json_data: str) -> 'Column':
        """
        Deserializes a JSON string to a Table object.
        """
        data = json.loads(json_data)
        t = Table()
        for k,v in data["Columns"].items():
            t.Columns[k] = Column(v["type"], v["options"])
            t.Columns[k].Data = v["data"]
        return t
    