from typing import Type
import json
class Column():
    def __init__(self,ctype) -> None:
        self.Type:__class__ = ctype
        self.Data:list[self.Type] = []
        
    def __len__(self) -> int:
        return len(self.Data)   
    def __getitem__(self, condition) -> 'Type':
        if isinstance(condition, self.Type):  # when you provide a single value
            return self.Data[condition]
        if isinstance(condition, list):  # when you provide a list of booleans
            return [value for value, cond in zip(self.Data, condition) if cond]
        return None  # for invalid conditions
    def __gt__(self, threshold):
        return [value > threshold for value in self.Data]
    def __lt__(self, threshold):
        return [value < threshold for value in self.Data]
    def __ge__(self, threshold):
        return [value >= threshold for value in self.Data]
    def __le__(self, threshold):
        return [value <= threshold for value in self.Data]
    def __eq__(self, threshold):
        return [value == threshold for value in self.Data]
    def __ne__(self, threshold):
        return [value != threshold for value in self.Data]
    def __contains__(self, values):
        return values in self.Data
    
    def between(self, start, end):
        return [start <= value <= end for value in self.Data]
    
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.Data[key] = value
        elif isinstance(key, list):
            for i in range(len(key)):
                if key[i]:
                    self.Data[i] = value
        else:
            raise Exception("Invalid Condition or Value")           
            
    
    def Add(self,*values):
        for value in values:
            if value.__class__ != self.Type and value != None:
                raise ValueError(f"Value {value} is not of type {self.Type}")
            self.Add(value)
    def RemoveFirst(self):
        self.Data.pop(0)
    def RemoveLast(self):
        self.Data.pop()
    def RemoveAll(self,value):
        self.Data = [i for i in self.Data if i != value]
    def RemoveAt(self,index):
        self.Data.pop(index)
    def RemoveIf(self,func):
        self.Data = [i for i in self.Data if not func(i)]
    
    def GetIf(self,func):
        return [i for i in self.Data if func(i)]
    
    def Get(self,index):
        #Read Only
        return self.Data[index]
    
    def Apply(self,func):
        self.Data = list(map(func,self.Data))
        
    def ApplyIf(self,func,condition):
        self.Data = [func(i) if condition(i) else i for i in self.Data]
        
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