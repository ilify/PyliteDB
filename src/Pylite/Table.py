import json

from regex import R
from .Column import Column
from .Types import *
from typing import Optional, Union, Type, Callable


class Table:
    PrintPadding = 1

    def __init__(self, TableName, SaveCallback=None):
        self.Columns: dict[str, Column] = {}
        self.TableName = TableName
        self.Save = SaveCallback

        # Events
        self.beforeInsert = None
        self.afterInsert = None
        self.beforeUpdate = None
        self.afterUpdate = None
        self.beforeDelete = None
        self.afterDelete = None
        self.beforeRenameColumn = None
        self.afterRenameColumn = None
        self.beforeRemoveColumn = None
        self.afterRemoveColumn = None
        self.beforeSelect = None
        self.afterSelect = None
        self.beforeSort = None
        self.afterSort = None
        self.beforeLimit = None
        self.afterLimit = None
        self.beforeAddColumn = None
        self.afterAddColumn = None
        self.beforeCopy = None
        self.afterCopy = None

    def __getitem__(self, Key) -> Union[list, Column]:
        if isinstance(Key, int):
            return self.Rows[Key]
        return self.Columns[Key]

    def __getattr__(self, name: str) -> Optional[Column]:
        if name in self.Columns:
            return self.Columns[name]
        raise AttributeError(f"Column '{name}' not found.")

    def AddColumn(self, **columns: Type):
        if self.beforeAddColumn != None:
            self.beforeAddColumn(self)
        for ColumnName, ColumnType in columns.items():
            # assert (
            #     ColumnType in PyliteTypes.SupportedTypes
            # ), f"Invalid type '{ColumnType}'"
            self.Columns[ColumnName] = Column(ColumnType, [], self.Save)
            setattr(
                self.__class__,
                ColumnName,
                property(lambda self: self.Tables[ColumnName]),
            )
        if self.Save != None:
            self.Save()
        if self.afterAddColumn != None:
            self.afterAddColumn(self)

    def RenameColumn(self, OldName, NewName):
        if self.beforeRenameColumn != None:
            self.beforeRenameColumn(self)
        self.Columns[NewName] = self.Columns.pop(OldName)
        setattr(self.__class__, NewName, property(lambda self: self.Columns[NewName]))
        delattr(self.__class__, OldName)
        if self.Save != None:
            self.Save()
        if self.afterRenameColumn != None:
            self.afterRenameColumn(self)

    def RemoveColumn(self, ColumnName):
        if self.beforeRemoveColumn != None:
            self.beforeRemoveColumn(self)
        del self.Columns[ColumnName]
        delattr(self.__class__, ColumnName)
        if self.Save != None:
            self.Save()
        if self.afterRemoveColumn != None:
            self.afterRemoveColumn(self)

    def Insert(self, **columns: Union[list, Type]):
        if self.beforeInsert != None:
            self.beforeInsert(self)
        for k, v in self.Columns.items():
            if k in list(columns.keys()):
                v.Add(v.Type(columns[k]))
            else:
                v.Add(v.Type())
        if self.Save != None:
            self.Save()
        if self.afterInsert != None:
            self.afterInsert(self)

    def Select(self, condition=None) -> "Table":
        if self.beforeSelect != None:
            self.beforeSelect(self)
        if condition == None:
            ret = self.Copy()
            if self.onSelect != None:
                self.onSelect(ret)
            return ret
        ReturnTable = Table("Selected Table")
        ReturnTable.Columns = {
            k: Column(v.Type, v.Options) for k, v in self.Columns.items()
        }
        for i in range(self.RowCount):
            if condition[i]:
                ReturnTable.Insert(
                    **{k: self.Rows[i][j] for j, k in enumerate(self.Columns.keys())}
                )
        if self.afterSelect != None:
            self.afterSelect(ReturnTable)
        return ReturnTable

    def Delete(self, index=None, where=None):
        if self.beforeDelete != None:
            self.beforeDelete(self)
        if self.isEmpty():
            raise ValueError("Table is empty.")
        if index == None and where == None:
            self.Columns = {
                k: Column(v.Type, v.Options) for k, v in self.Columns.items()
            }
        if index != None:
            [v.RemoveAt(index) for v in self.Columns.values()]
        if where != None:
            [x.RemoveByList(where) for x in self.Columns.values()]
        if self.Save != None:
            self.Save()
        if self.afterDelete != None:
            self.afterDelete(self)

    def Update(self, index=None, where=None, **columns: Union[list, Type]):
        if self.beforeUpdate != None:
            self.beforeUpdate(self)
        if index == None and where == None:
            for k, v in columns.items():
                self.Columns[k].Data = [v for _ in self.Columns[k].Data]
        if index != None:
            for k, v in columns.items():
                self.Columns[k].Data[index] = v
        if where != None:
            for k, v in columns.items():
                for i in range(len(where)):
                    if where[i]:
                        self.Columns[k].Data[i] = v
        if self.Save != None:
            self.Save()
        if self.afterUpdate != None:
            self.afterUpdate(self)

    def isEmpty(self) -> bool:
        return all([col.isEmpty() for col in self.Columns.values()])

    def __str__(self) -> str:
        if self.isEmpty():
            return f"Table is empty."

        def getMaxLength(column) -> int:
            return max([len(str(x)) for x in column.Data])

        def formatCell(cell, maxLen):
            return f" {cell} {' '*(maxLen-len(str(cell)))}"

        maxLenperColumn = [
            max(getMaxLength(col), len(key)) + self.PrintPadding
            for col, key in zip(self.Columns.values(), self.Columns.keys())
        ]
        numberOfLines = max([len(col.Data) for col in self.Columns.values()])
        ret = f"{self.TableName} ({self.Length} Entries):\n"
        ret += (
            "|"
            + "|".join(
                [
                    formatCell(list(self.Columns.keys())[i], maxLenperColumn[i])
                    for i in range(len(self.Columns))
                ]
            )
            + "|\n"
        )
        ret += (
            "|"
            + "|\n|".join(
                "|".join(
                    (formatCell(col.Data[i], maxLen) if col.Type != bytes else "BLOB")
                    for col, maxLen in zip(self.Columns.values(), maxLenperColumn)
                )
                for i in range(numberOfLines)
            )
            + "|"
        )
        return ret

    @property
    def Rows(self) -> list:
        return [
            {key: col.Data[i] for key, col in self.Columns.items()}
            for i in range(len(self.Columns[list(self.Columns.keys())[0]].Data))
        ]

    @property
    def Length(self) -> int:
        return self.RowCount

    def __len__(self) -> int:
        return self.RowCount

    def GetColumns(self) -> list:
        return list(self.Columns.keys())

    def Exists(self, **columns: Union[list, Type]) -> bool:
        for k, v in columns.items():
            if k not in self.Columns.keys():
                return False
            if v not in self.Columns[k].Data:
                return False
        return True

    @property
    def RowCount(self) -> int:
        return len(self.Rows)

    def Limit(self, n):
        if self.beforeLimit != None:
            self.beforeLimit(self)
        T = Table(self.TableName, self.Save)
        T.Columns = {k: Column(v.Type, v.Options) for k, v in self.Columns.items()}
        for i in range(min(n, self.RowCount)):
            T.Insert(**{k: v.Data[i] for k, v in self.Columns.items()})
        if self.afterLimit != None:
            self.afterLimit(T)
        return T

    def Sort(self, Column, Reverse=False):
        if self.beforeSort != None:
            self.beforeSort(self)
        if Column not in self.Columns.keys():
            raise ValueError(f"Column '{Column}' not found.")
        T = self.Copy()
        sorted_indices = sorted(
            range(len(T.Columns[Column].Data)),
            key=lambda i: T.Columns[Column].Data[i],
            reverse=Reverse,
        )
        for col in T.Columns.values():
            col.Data = [col.Data[i] for i in sorted_indices]
        if self.afterSort != None:
            self.afterSort(T)
        return T

    def Copy(self):
        if self.beforeCopy != None:
            self.beforeCopy(self)
        T = Table(self.TableName, self.Save)
        T.Columns = {k: Column(v.Type, v.Options) for k, v in self.Columns.items()}
        for i in range(self.RowCount):
            T.Insert(**{k: v.Data[i] for k, v in self.Columns.items()})
        if self.afterCopy != None:
            self.afterCopy(T)
        return T

    def toJson(self):
        return {"Columns": {k: v.toJson() for k, v in self.Columns.items()}}
