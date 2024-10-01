from typing import Type

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
            
    
    def Add(self,value):
        if value.__class__ != self.Type:
            raise ValueError(f"Value {value} is not of type {self.Type}")
        self.Data.append(value)
    def AddAll(self,*values):
        for value in values:
            self.Add(value)
    def RemoveFirst(self):
        self.Data.pop(0)
    def RemoveLast(self):
        self.Data.pop()
    def RemoveAll(self,value):
        self.Data = [i for i in self.Data if i != value]
    def RemoveAt(self,index):
        self.Data.pop(index)
    def Removeif(self,func):
        self.Data = [i for i in self.Data if not func(i)]
    
    def Getif(self,func):
        return [i for i in self.Data if func(i)]
    
    def Get(self,index):
        return self.Data[index]
    
    def Apply(self,func):
        self.Data = list(map(func,self.Data))
        
    def __str__(self) -> str:
        data = ""
        max_len = len(str(len(self.Data)))
        for i in range(len(self.Data)):
            data += f"{str(i).ljust(max_len)} | " + f"{self.Data[i]}\n"
        return (f"Column {self.Type} with {len(self)} elements \n{data[:-1] if data else 'Empty'}")
    
    