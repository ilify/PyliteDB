from math import e
from random import randint
from matplotlib import table
import pandas as pd
from typing import Type
from faker import Faker
from pyparsing import C
import dill

from .Tools import print_warning


class Table:
    def __init__(self, TableName="", SaveCallback=None):
        self.Data = pd.DataFrame()
        self.TableName = TableName
        self.Save = SaveCallback
        self.PrimaryKey = None
        self.ForeignKeys = {}
        self.isLinked = False
        self.FakeData = Faker()
        self.ColumnTypes = {}
        # region Events
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
        self.beforeAddColumn = None
        self.afterAddColumn = None
        self.beforeCopy = None
        self.afterCopy = None
        # endregion




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
        for _, row in self.Data.iterrows():
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
            return DictObj(self.Data.iloc[Key])
        return self.Data[Key]

    # region CRUD
    def AddColumn(self, **columns: Type):
        if self.beforeAddColumn:
            self.beforeAddColumn(self)
        for ColumnName, ColumnType in columns.items():
            self.Data[ColumnName] = pd.Series()
            self.ColumnTypes[ColumnName] = ColumnType
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
            
        
        if(list(self.Columns) not in list(columns.keys())):
            missing_columns = list(set(self.Columns) - set(columns.keys()))
            extra_columns = list(set(columns.keys()) - set(self.Columns))
            if len(missing_columns) > 0 :
                print_warning(f"Warning on Insert : the flowing columns are missing ({", ".join(missing_columns)}) They will be filled with None instead")
            if len(extra_columns) > 0:
                print_warning(f"Warning on Insert : {self.TableName} has no column named ({", ".join(extra_columns)}) They will be ignored")
            #remove extra columns and add missing columns
            for col in extra_columns:
                del columns[col]
            for col in missing_columns:
                columns[col] = None
            
        for col, val in columns.items():
            if not isinstance(val, self.ColumnTypes[col]) and val is not None:
                columns[col] = self.ColumnTypes[col](val)

        self.Data = pd.concat([self.Data, pd.DataFrame([columns])], ignore_index=True)
        if self.Save:
            self.Save()
        if self.afterInsert:
            self.afterInsert(self, DictObj(columns))
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

    def Get(self, **columns):
        if self.beforeSelect:
            self.beforeSelect(self)
        condition = pd.Series([True] * len(self.Data))
        for col, val in columns.items():
            condition &= self.Data[col] == val
        try:
            result = self.Data[condition].to_dict(orient="records")[0]
        except IndexError:
            result = {}
        if self.afterSelect:
            self.afterSelect(self)
        return DictObj(result) if result != {} else None

    def Delete(self, condition=None, index=None, all=False):
        if self.beforeDelete:
            self.beforeDelete(self)

        deleted_rows = None

        if all:
            deleted_rows = self.Data.copy()
            cols = self.Data.columns
            types = [s.dtype for s in self.Data.values.T]
            self.Data = pd.DataFrame()
            self.AddColumn(**{col: dtype for col, dtype in zip(cols, types)})

        if index is not None:
            deleted_rows = self.Data.iloc[[index]].copy()
            self.Data = self.Data.drop(index).reset_index(
                drop=True
            )  # Remove row by index

        if condition is not None:
            deleted_rows = self.Data[condition].copy()
            self.Data = self.Data[~condition].reset_index(
                drop=True
            )  # Remove rows based on the inverse of the condition

        if self.Save:
            self.Save()
        if self.afterDelete:
            self.afterDelete(self)
        if self.isLinked:
            self.__LinkedDelete__(deleted_rows)

    def DeleteAt(self, index):
        if self.beforeDelete:
            self.beforeDelete(self)
        deleted_rows = self.Data.iloc[[index]].copy()
        self.Data = self.Data.drop(index).reset_index(drop=True)
        if self.Save:
            self.Save()
        if self.afterDelete:
            self.afterDelete(self)
        # print(deleted_rows)
        if self.isLinked:
            self.__LinkedDelete__(deleted_rows)

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

    # endregion
    # region Properties
    @property
    def Columns(self) -> list:
        return list(self.ColumnTypes.keys())

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

    # endregion
    # region Extra
    def Exists(self, **columns) -> bool:
        if self.isEmpty(): return False
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


    def toDict(self):
        """Convert table to a serializable dictionary"""
        return {
            "TableName": self.TableName,
            "Data": self.Data.to_dict(orient='records'),
            "PrimaryKey": self.PrimaryKey,
            "ForeignKeys": self.ForeignKeys,
            "isLinked": self.isLinked,
            "ColumnTypes": self.ColumnTypes,
            "Events": {
                "beforeInsert": dill.dumps(self.beforeInsert),
                "afterInsert": dill.dumps(self.afterInsert),
                "beforeUpdate": dill.dumps(self.beforeUpdate),
                "afterUpdate": dill.dumps(self.afterUpdate),
                "beforeDelete": dill.dumps(self.beforeDelete),
                "afterDelete": dill.dumps(self.afterDelete),
                "beforeRenameColumn": dill.dumps(self.beforeRenameColumn),
                "afterRenameColumn": dill.dumps(self.afterRenameColumn),
                "beforeRemoveColumn": dill.dumps(self.beforeRemoveColumn),
                "afterRemoveColumn": dill.dumps(self.afterRemoveColumn),
                "beforeSelect": dill.dumps(self.beforeSelect),
                "afterSelect": dill.dumps(self.afterSelect),
                "beforeAddColumn": dill.dumps(self.beforeAddColumn),
                "afterAddColumn": dill.dumps(self.afterAddColumn),
                "beforeCopy": dill.dumps(self.beforeCopy),
                "afterCopy": dill.dumps(self.afterCopy)
            }
        }

    
    def loadFromDict(self, data):
        """Load table data from a dictionary"""
        self.TableName = data["TableName"]
        self.Data = pd.DataFrame(data["Data"])
        self.PrimaryKey = data["PrimaryKey"]
        self.ForeignKeys = data["ForeignKeys"]
        self.isLinked = data["isLinked"]
        self.ColumnTypes = data["ColumnTypes"]
        
        # Restore events
        events = data["Events"]
        for event_name, event_bytes in events.items():
            if event_bytes is not None:
                setattr(self, event_name, dill.loads(event_bytes))
        
        # Recreate property accessors for columns
        for column in self.Data.columns:
            setattr(
                self.__class__,
                column,
                property(lambda self, col=column: self.Data[col])
            )
            self.Data[column].__setattr__("parent", self.TableName)  # needed for linking
        
        return self

    def SaveToDisk(self, path):
        """Save the table to disk"""
        try:
            with open(path, 'wb') as f:
                dill.dump(self.toDict(), f)
            return True
        except Exception as e:
            print(f"Error saving table: {e}")
            return False

    def LoadFromDisk(self, path):
        """Load table data from disk into the current instance"""
        try:
            with open(path, 'rb') as f:
                data = dill.load(f)
            return self.loadFromDict(data)
        except Exception as e:
            print(f"Error loading table: {e}")
            return None

    # endregion

    # region Linking
    def LinkTo(self, pk, table, on):
        self.isLinked = True
        self.PrimaryKey = pk
        self.ForeignKeys[table] = on

    def __LinkedDelete__(self, deletedRows):
        for table, on in self.ForeignKeys.items():
            table.Delete(condition=table.Data[on].isin(deletedRows[self.PrimaryKey]))

    # endregion

    # region Fake Data
    def GenerateFake(self,n):
        nativeTypes = [int, float, str, bool]
        for i in range(n):
            col = {}
            for k,v in self.ColumnTypes.items():
                if v in nativeTypes:
                    if v == int:
                        col[k] = randint(-1000000,1000000)
                    elif v == float:
                        col[k] = randint(-1000000,1000000)/100
                    elif v == str:
                        col[k] = self.FakeData.word()
                    elif v == bool:
                        col[k] = randint(0,1) == 1
                else:
                    col[k] = v.fake()
            
            self.Insert(**col)
            
            # col = {k:v.fake() for k,v in self.ColumnTypes}
            # print(col)
            
    # endregion

class DictObj:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    
    def __iter__(self):
        return iter(self.__dict__.items())
    
    def __str__(self):
        return str(self.__dict__)

