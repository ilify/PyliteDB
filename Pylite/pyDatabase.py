import json
from typing import Optional

from Pylite.pyColumn import Column
from .pyTable import Table
from .pyTools import *

class Database():
    def __init__(self,path="",password=""):
        self.Tables = {}
        if path != "":
            self.path = path
            self.password = password
            try:
                self.Load()
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{path}' not found.")
            except Exception as e:
                raise SystemExit(f"Incorrect Password")
    
    def __getattr__(self, name: str) -> Optional[Table]:
        if name in self.Tables:
            return self.Tables[name]
        raise AttributeError(f"Table '{name}' not found.")
    
    def GetTables(self):
        return list(self.Tables.keys())
    
    def CreateTable(self,TableName) -> Table:
        self.Tables[TableName] = Table(TableName)
        setattr(self.__class__, TableName, property(lambda self: self.Tables[TableName]))
        return self.Tables[TableName]
    
    def RenameTable(self,OldName,NewName):
        self.Tables[NewName] = self.Tables.pop(OldName)
        self.Tables[NewName].TableName = NewName
        setattr(self.__class__, NewName, property(lambda self, name=NewName: self.Tables[name]))
        delattr(self.__class__, OldName)
    
    def DeleteTable(self,TableName):
        del self.Tables[TableName]
        delattr(self.__class__, TableName)
    
    def __len__(self) -> int:
        return len(self.Tables.keys())
    
    def Load(self):
        with open(self.path,"r") as f:
            data = json.loads(decrypt(f.read(),self.password))
            for k,v in data["Tables"].items():
                t = self.CreateTable(k)
                for c in v["Columns"].keys():
                    
                    t.Columns[c] = Column(eval(v["Columns"][c]["Type"]),v["Columns"][c]["Options"])
                    t.Columns[c].Data = v["Columns"][c]["Data"]
    
    def Save(self,Path,Password=""):
        if Password != "":
            self.password = Password
        file = json.dumps({
            "Tables": {k:{
                "Columns":{c:{
                    "Type":v.Columns[c].Type.__name__,
                    "Data":v.Columns[c].Data,
                    "Options":v.Columns[c].Options
                    } for c in v.Columns.keys()}
                } for k,v in self.Tables.items()}
        })
        with open(Path,"w") as f:
            f.write(encrypt(file,self.password))
        
    def ChangePassword(self,Password):
        self.password = Password
        self.Save(self.path,Password)
        

            
    