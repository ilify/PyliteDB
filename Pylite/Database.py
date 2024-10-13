import json
from typing import Optional
import sqlite3
from Pylite.Column import Column
from .Table import Table
from .Tools import *

class Database():
    def __init__(self, Path="", Password="", AutoSave=False):
        self.Tables = {}
        self.password = Password
        self.path = Path
        self.autosave = AutoSave
        if self.path != "":
            try:
                self.Load()
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{self.path}' not found.")
            except Exception as e:
                raise e
        
    
    def GetTables(self):
        return list(self.Tables.keys())
    
    def CreateTable(self, TableName) -> Table:
        self.Tables[TableName] = Table(TableName,self.SaveIfPossible)
        setattr(self.__class__, TableName, property(lambda self: self.Tables[TableName]))
        self.SaveIfPossible()
        return self.Tables[TableName]
    
    
    # @NotImplemented
    # def CreateTableForClass(self, TableName, Class) -> Table:
    #     self.Tables[TableName] = Table(TableName, self.autosave_callback if self.autosave else None)
    #     self.Tables[TableName].AddColumn(**Class.__dict__)
    #     setattr(Class, TableName, property(lambda self: self.Tables[TableName]))
    #     self.SaveIfPossible()
    #     return self.Tables[TableName]
    
    def RenameTable(self,OldName,NewName):
        self.Tables[NewName] = self.Tables.pop(OldName)
        self.Tables[NewName].TableName = NewName
        setattr(self.__class__, NewName, property(lambda self, name=NewName: self.Tables[name]))
        delattr(self.__class__, OldName)
        self.SaveIfPossible()
    
    def DeleteTable(self,TableName):
        del self.Tables[TableName]
        delattr(self.__class__, TableName)
        
    def __len__(self) -> int:
        return len(self.Tables.keys())
    
    def Load(self):
        wasOnAutoSave = self.autosave
        self.autosave = False
        fromJson = False
        if self.password == "" : fromJson = True
        try:
            with open(self.path,"r") as f:
                if fromJson:
                    data = json.loads(f.read())
                else:
                    data = json.loads(decrypt(f.read(),self.password))
                for k,v in data["Tables"].items():
                    t = self.CreateTable(k)
                    for c in v["Columns"].keys():
                        t.Columns[c] = Column(eval(v["Columns"][c]["Type"]),v["Columns"][c]["Options"],self.Save)
                        t.Columns[c].Data = v["Columns"][c]["Data"]
            self.autosave = wasOnAutoSave
        except Exception as e:
            raise SystemExit("Error while Loading Database : Incorrect Password" if self.password != "" else "Error while Loading Database : Database is Locked - Please Make Sure You Provide a Password :\n Database(Path,YOUR_PASSWORD_HERE)")
    
    
    def LoadFromSQL(self,SQLFilePath):
        SQL_TYPE_MAP = {
            "INTEGER":int,
            "REAL":float,
            "TEXT":str,
            "BLOB":bytes
        }
        conn = sqlite3.connect(SQLFilePath)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [x[0] for x in c.fetchall() if x[0] != "sqlite_sequence"]
        for table in tables:
            t = self.CreateTable(table)
            c.execute(f"PRAGMA table_info({table})")
            columns = {x[1]:SQL_TYPE_MAP[x[2]] for x in c.fetchall()}
            t.AddColumn(**columns)
            for column in columns:
                t.Columns[column].Data = [x[0] for x in c.execute(f"SELECT {column} FROM {table}").fetchall()]
        conn.close()
    
    def Save(self,Path="",Password="",asJson=False):
        if self.path == "" and Path == "":
            raise SystemExit("Error while Saving Database : No path provided")
        
        if self.path == "":
            self.path = Path
        if self.password == "":
            self.password = Password
        
        file = json.dumps(self.toJson())
        with open(self.path,"w") as f:
            if asJson:
                f.write(file)
            else:
                f.write(encrypt(file,self.password))
        
    def ChangePassword(self,Password):
        self.password = Password

    def SaveIfPossible(self):
        if self.autosave: self.Save()
            
    def toJson(self):
        Tables = {k:v.toJson() for k,v in self.Tables.items()}
        return {"Tables":Tables }
            
    