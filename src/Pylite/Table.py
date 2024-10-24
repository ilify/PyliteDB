from h11 import Data
import pandas as pd
from typing import Type
from faker import Faker


class Table:
    def __init__(self, TableName, SaveCallback=None):
        self.Data = pd.DataFrame()
        self.TableName = TableName
        self.Save = SaveCallback
        self.FakeData = Faker()
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

    def __str__(self) -> str:
        PrintPadding = 1
        if self.isEmpty():
            return f"Table '{self.TableName}' is empty."

        # Get the max length for each column
        # Calculate the maximum length for each column, including the column name
        max_len_per_column = (
            self.Data.map(lambda x: len(str(x)))
            .max()  # Get max length of each value
            .combine(
                self.Data.columns.to_series().apply(len), max
            )  # Compare with column names
        ) + PrintPadding

        # Create a dictionary with the maximum lengths per column
        column_lengths = {
            col: max_len for col, max_len in zip(self.Data.columns, max_len_per_column)
        }

        # Prepare header (column names)
        header = (
            "| "
            + " | ".join([col.ljust(column_lengths[col]) for col in self.Data.columns])
            + " |"
        )

        # Prepare the separator (dashes)
        separator = (
            "•-"
            + "-•-".join(["-" * column_lengths[col] for col in self.Data.columns])
            + "-•"
        )

        # Prepare rows
        rows = ""
        for i, row in self.Data.iterrows():
            row_cells = [
                str(cell).ljust(column_lengths[col]) for col, cell in row.items()
            ]
            rows += "| " + " | ".join(row_cells) + " |\n"

        # Construct the final output
        table_str = f"{self.TableName} ({len(self.Data)} Entries):\n"
        table_str += separator + "\n"
        table_str += header + "\n"
        table_str += separator + "\n"
        table_str += rows
        table_str += separator

        return table_str

    def __getattr__(self, name):
        if name in ["Data", "TableName", "Save", "FakeData"]:
            return object.__getattribute__(self, name)
        return self.Data[name]

    def __getitem__(self, Key):
        if isinstance(Key, int):
            return self.Data.iloc[Key]
        return self.Data[Key]

    def AddColumn(self, **columns: Type):
        if self.beforeAddColumn:
            self.beforeAddColumn(self)
        for ColumnName, ColumnType in columns.items():
            self.Data[ColumnName] = pd.Series(dtype=ColumnType)
            setattr(
                self.__class__,
                ColumnName,
                property(lambda self, ColumnName=ColumnName: self.Data[ColumnName]),
            )
        if self.Save:
            self.Save()
        if self.afterAddColumn:
            self.afterAddColumn(self)
        return self

    def RenameColumn(self, OldName, NewName):
        if self.beforeRenameColumn:
            self.beforeRenameColumn(self)
        self.Data = self.Data.rename(columns={OldName: NewName})
        setattr(
            self.__class__,
            NewName,
            property(lambda self, NewName=NewName: self.Data[NewName]),
        )
        delattr(self.__class__, OldName)
        if self.Save:
            self.Save()
        if self.afterRenameColumn:
            self.afterRenameColumn(self)
        return self

    def RemoveColumn(self, ColumnName):
        if self.beforeRemoveColumn:
            self.beforeRemoveColumn(self)
        delattr(self.__class__, ColumnName)
        self.Data = self.Data.drop(columns=[ColumnName])
        if self.Save:
            self.Save()
        if self.afterRemoveColumn:
            self.afterRemoveColumn(self)
        return self

    def Insert(self, **columns):
        if self.beforeInsert:
            self.beforeInsert(self)
        self.Data = pd.concat([self.Data, pd.DataFrame([columns])], ignore_index=True)
        if self.Save:
            self.Save()
        if self.afterInsert:
            self.afterInsert(self)
        return self

    def Select(self, condition=None) -> "Table":
        if self.beforeSelect:
            self.beforeSelect(self)
        if condition is None:
            return self.Copy()
        ReturnTable = Table("Selected Table")
        ReturnTable.Data = self.Data[condition].copy()
        if self.afterSelect:
            self.afterSelect(self)
        return ReturnTable

    def Delete(self, condition=None, index=None, all=False):
        if self.beforeDelete:
            self.beforeDelete(self)

        if all == True:
            cols = self.Data.columns
            types = [s.dtype for s in self.Data.values.T]
            self.Data = pd.DataFrame()
            self.AddColumn(**{col: dtype for col, dtype in zip(cols, types)})
            

        if index is not None:
            self.Data = self.Data.drop(index).reset_index(
                drop=True
            )  # Remove row by index

        if condition is not None:
            self.Data = self.Data[~condition].reset_index(
                drop=True
            )  # Remove rows based on the inverse of the condition

        if self.Save:
            self.Save()
        if self.afterDelete:
            self.afterDelete(self)

    def DeleteAt(self, index):
        if self.beforeDelete:
            self.beforeDelete(self)
        self.Data = self.Data.drop(index).reset_index(drop=True)
        if self.Save:
            self.Save()
        if self.afterDelete:
            self.afterDelete(self)

    def Update(self, selector=None, **columns):
        if self.beforeUpdate:
            self.beforeUpdate(self)
        if selector is None:
            # Update entire columns with the same value across all rows
            for k, v in columns.items():
                self.Data[k] = [v] * len(self.Data)
        else:
            # Update rows based on selector
            for k, v in columns.items():
                self.Data.loc[selector, k] = v
        if self.Save:
            self.Save()
        if self.afterUpdate:
            self.afterUpdate(self)

    def UpdateAt(self, index, **columns):
        if self.beforeUpdate:
            self.beforeUpdate(self)
        for k, v in columns.items():
            self.Data.at[index, k] = v
        if self.Save:
            self.Save()
        if self.afterUpdate:
            self.afterUpdate(self)

    def RemoveDuplicates(self):
        self.Data = self.Data.drop_duplicates()
        return self

    def isEmpty(self):
        return self.Data.empty

    @property
    def Columns(self):
        return self.Data.columns.values

    @property
    def Rows(self):
        return self.Data.values.tolist()

    @property
    def Length(self):
        return len(self.Data)

    @property
    def df(self):
        return self.Data

    def __len__(self):
        return len(self.Data)

    def Exists(self, **columns):
        for k, v in columns.items():
            if not self.Data[k].isin([v]).any():
                return False
        return True

    def Limit(self, n):
        self.Data = self.Data.head(n)
        return self

    def Sort(self, Column, ascending=True):
        self.Data = self.Data.sort_values(by=Column, ascending=ascending)
        return self

    def Copy(self):
        T = Table(self.TableName, self.Save)
        T.Data = self.Data.copy()
        return T

    def ColumnStats(self, column):
        return self.Data[column].describe()

    def Difference(self, OtherTable):
        return self.Data.compare(OtherTable.Data)

    def Intersection(self, OtherTable, onColumn=None):
        if onColumn:
            return pd.merge(self.Data, OtherTable.Data, how="inner", on=onColumn)
        return pd.merge(self.Data, OtherTable.Data, how="inner")

    def Union(self, OtherTable):
        return pd.concat([self.Data, OtherTable.Data]).drop_duplicates()

    def Distinct(self, Column):
        return self.Data[Column].unique()

    def ReorderColumns(self, NewOrder):
        self.Data = self.Data[NewOrder]
        return self

    def Map(self, Column, Mapping):
        self.Data[Column] = self.Data[Column].map(Mapping)
        return self

    def toJson(self):
        return self.Data.to_json()

    def LoadFromJson(self, json):
        from io import StringIO

        json_data = StringIO(json)
        self.Data = pd.read_json(json_data)
