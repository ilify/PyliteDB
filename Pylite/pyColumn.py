from typing import Type
import json
class Column():
    def __init__(self,ctype,options = []) -> None:
        self.Type:__class__ = ctype
        self.Data:list[self.Type] = []
        self.Options:list[str] = options
        
    def __gt__(self,other) -> bool:
        return [value > other for value in self.Data ]
    
    def __lt__(self, other) -> list:
        return [value < other for value in self.Data]

    def __eq__(self, other) -> list:
        return [value == other for value in self.Data]

    def __ge__(self, other) -> list:
        return [value >= other for value in self.Data]

    def __le__(self, other) -> list:
        return [value <= other for value in self.Data]

    def __ne__(self, other) -> list:
        return [value != other for value in self.Data]
    
    def between(self,min,max) -> list:
        return [value > min and value < max for value in self.Data]
    
    
    
    def __len__(self) -> int:
        return len(self.Data)   
    def Add(self,*values) -> None:
        for value in values:
            if value.__class__ != self.Type and value != None:
                raise ValueError(f"Value {value} is not of type {self.Type}")
            self.Data.append(value)
    def RemoveFirst(self) -> None:
        self.Data.pop(0)
    def RemoveLast(self) -> None:
        self.Data.pop()
    def RemoveAll(self,value) -> None:
        self.Data = [i for i in self.Data if i != value]
    def RemoveAt(self,index) -> None:
        self.Data.pop(index)
    def RemoveIf(self,func) -> None:
        self.Data = [i for i in self.Data if not func(i)]
    def RemoveByList(self,values) -> None:
        self.Data = [self.Data[i] for i in range(len(self.Data)) if values[i] == False]
    def GetIf(self,func) -> list:
        return [i for i in self.Data if func(i)]
    def Get(self,index) -> 'Type':
        #Read Only
        return self.Data[index]
    def Apply(self,func) -> None:
        self.Data = list(map(func,self.Data))
    def ApplyIf(self,func,condition) -> None:
        self.Data = [func(i) if condition(i) else i for i in self.Data]
    def ReType(self,newType:Type) -> None:
        self.Data = [newType(i) for i in self.Data]
        self.Type = newType
    def isEmpty(self) -> bool:
        return len(self.Data) == 0
    def __str__(self) -> str:
        data = ""
        max_len = len(str(len(self.Data)))
        for i in range(len(self.Data)):
            data += f"{str(i).ljust(max_len)} | " + f"{self.Data[i]}\n"
        return (f"Column {self.Type} with {len(self)} elements \n{data[:-1] if data else 'Empty'}")
    def serialize(self) -> str:
        """
        Serializes the Column object to a JSON string.
        """
        return json.dumps({
            'type': self.Type.__name__,  # Store the type name as a string
            'data': self.Data
        })
    @staticmethod
    def deserialize(json_data: str) -> 'Column':
        """
        Deserializes a JSON string to a Column object.
        """
        data = json.loads(json_data)
        column_type = eval(data['type'])  # Converts string back to type
        column = Column(column_type)
        column.Data = data['data']
        return column