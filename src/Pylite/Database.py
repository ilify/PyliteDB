import json
from typing import Optional
import sqlite3
from .Table import Table
from .Tools import *
import pandas as pd


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
            with open(self.path, "r") as f:
                if fromJson:
                    data = json.loads(f.read())
                else:
                    data = json.loads(decrypt(f.read(), self.password))
                for k, v in data["Tables"].items():
                    t = self.CreateTable(k)
                    t.LoadFromJson(v)
            self.autosave = wasOnAutoSave
        except Exception as e:
            raise SystemExit(
                "Error while Loading Database : Incorrect Password"
                if self.password != ""
                else "Error while Loading Database : Database is Locked - Please Make Sure You Provide a Password :\n Database(Path,YOUR_PASSWORD_HERE)"
            )

    def LoadFromSQL(self, SQLFilePath):
        conn = sqlite3.connect(SQLFilePath)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [x[0] for x in c.fetchall() if x[0] != "sqlite_sequence"]
        for table in tables:
            t = self.CreateTable(table)
            t.Data = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        conn.close()

    def Save(self, Path="", Password="", asJson=False):
        if self.path == "" and Path == "":
            raise SystemExit("Error while Saving Database : No path provided")

        if self.path == "":
            self.path = Path
        if self.password == "":
            self.password = Password

        file = json.dumps(self.toJson())
        with open(self.path, "w") as f:
            if asJson:
                f.write(file)
            else:
                f.write(encrypt(file, self.password))

    def ChangePassword(self, Password):
        self.password = Password

    def SaveIfPossible(self):
        if self.autosave:
            self.Save()

    def toJson(self):
        Tables = {}
        for k, v in self.Tables.items():
            Tables[k] = v.toJson()
        return {"Tables": Tables}

    def __str__(self):
        indexes = iter(range(0, len(self.GetTables())))
        tables_list = "\n ".join(
            [f"{next(indexes)} - {table}" for table in self.GetTables()]
        )
        print(f"Database '{self.path}' Contains {len(self)} Tables :\n {tables_list}")
        TableToPrint = input("Select Table To Display (use index or name) : ")
        try:
            index = int(TableToPrint)
            Table = self.GetTables()[index]
            print(self.Tables[Table])
        except:
            print(self.Tables[TableToPrint])
        return "\b"
