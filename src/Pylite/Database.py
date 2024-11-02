import json
from typing import Optional
import sqlite3

from .Table import Table
from .Tools import *
import pandas as pd
import dill


class Database:
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

    def __getitem__(self, Key) -> Table:
        return self.Tables[Key]

    def __getattr__(self, name: str) -> Optional[Table]:
        if name in self.Tables:
            return self.Tables[name]
        raise AttributeError(f"Table '{name}' not found.")

    def GetTables(self):
        return list(self.Tables.keys())

    def ClearEmptyTables(self):
        for k in list(self.Tables.keys()):
            if self.Tables[k].isEmpty():
                self.DeleteTable(k)
        self.SaveIfPossible()

    def CreateTable(self, TableName) -> Table:
        self.Tables[TableName] = Table(TableName, self.SaveIfPossible)
        setattr(
            self.__class__, TableName, property(lambda self: self.Tables[TableName])
        )
        self.SaveIfPossible()
        return self.Tables[TableName]

    def RenameTable(self, OldName, NewName):
        self.Tables[NewName] = self.Tables.pop(OldName)
        self.Tables[NewName].TableName = NewName
        setattr(
            self.__class__,
            NewName,
            property(lambda self, name=NewName: self.Tables[name]),
        )
        delattr(self.__class__, OldName)
        self.SaveIfPossible()

    def DeleteTable(self, TableName):
        del self.Tables[TableName]
        delattr(self.__class__, TableName)

    def __len__(self) -> int:
        return len(self.Tables.keys())

    def Load(self):
        wasOnAutoSave = self.autosave
        self.autosave = False
        fromJson = False
        if self.password == "":
            fromJson = True
            
        try:
            with open(self.path, "rb") as f:  # Changed to 'rb' for binary reading
                if fromJson:
                    data = dill.load(f)
                else:
                    encrypted_data = f.read()
                    decrypted_data = decrypt(encrypted_data, self.password)
                    data = dill.loads(decrypted_data)
                    
                
                for table_name, table_data in data["Tables"].items():
                    table = self.CreateTable(table_name)
                    table.loadFromDict(table_data)
                    
            self.autosave = wasOnAutoSave
        except Exception as e:
            raise SystemExit(
                "Error while Loading Database: Incorrect Password"
                if self.password != ""
                else "Error while Loading Database: Database is Locked - Please Make Sure You Provide a Password:\n Database(Path,YOUR_PASSWORD_HERE)"
            )

    @staticmethod
    def LoadFromSQL(SQLFilePath) -> 'Database':
        db = Database()
        conn = sqlite3.connect(SQLFilePath)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [x[0] for x in c.fetchall() if x[0] != "sqlite_sequence"]
        for table in tables:
            t = db.CreateTable(table)
            t.Data = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        conn.close()
        return db

    def Save(self, Path="", Password="", asJson=False):
        if self.path == "" and Path == "":
            raise SystemExit("Error while Saving Database: No path provided")

        if self.path == "":
            self.path = Path
        if self.password == "":
            self.password = Password

        data = self.toDict()
        
        with open(self.path, "wb") as f:  # Changed to 'wb' for binary writing
            if asJson:
                dill.dump(data, f)
            else:
                serialized_data = dill.dumps(data)
                encrypted_data = encrypt(serialized_data, self.password)
                f.write(encrypted_data)

    def ChangePassword(self, Password):
        self.password = Password

    def SaveIfPossible(self):
        if self.autosave:
            self.Save()

    def Link(self, source, target):
        source_table = self.Tables[source.parent]
        if isinstance(target, list):
            for targetcol in target:
                source_table.LinkTo(source.name, self.Tables[targetcol.parent], targetcol.name)
        elif isinstance(target, pd.Series):
            source_table.LinkTo(source.name, self.Tables[target.parent], target.name)
        
    def toDict(self):
        """Convert database to a serializable dictionary"""
        return {
            "Tables": {
                name: table.toDict() 
                for name, table in self.Tables.items()
            }
        }

    def __str__(self):
        indexes = iter(range(0, len(self.GetTables())))
        tables_list = "\n ".join(
            [f"{next(indexes)} - {table}" for table in self.GetTables()]
        )
        print(f"Database '{self.path}' Contains {len(self)} Tables:\n {tables_list}")
        TableToPrint = input("Select Table To Display (use index or name): ")
        try:
            index = int(TableToPrint)
            Table = self.GetTables()[index]
            print(self.Tables[Table])
        except:
            print(self.Tables[TableToPrint])
        return "\b"
