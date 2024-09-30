import inspect
import pandas as pd
import numpy as np
import json
import sys
import traceback
sys.tracebacklimit = 0

class Database():
    def __init__(self):
        self.Tables = {}
        
    def __getitem__(self,Key):
        return self.Tables[Key]
    
    def CreateTable(self,TableName) -> pd.DataFrame:
        self.Tables[TableName] = Table()
        self.add_property(TableName)
        return self.Tables[TableName]
    
    def __len__(self) -> int:
        return len(self.Tables.keys())
    
    def add_property(self, name):
        setattr(self.__class__, name, property(lambda self: self.Tables[name]))
    
    
class Table(pd.DataFrame):
    def __init__(self):
        super().__init__()
        
    def AddColumns(self,**Columns):
        for Name,Type in Columns.items():
            self[Name] = pd.Series(dtype=Type)
        return self
    
    def Insert(self,**Data):
        Row = [Data[i] if i in Data else np.nan for i in self.columns]
        self.loc[len(self)] = Row
        
        
    def Delete(self,Condition):
        self.drop(self[Condition].index,inplace=True)
    
    def __getitem__(self,Key) -> pd.Series:
        try:
            return super().__getitem__(Key)
        except :
            raise SystemExit(bcolors.FAIL+f"Pylite Error : Column '{Key}' does not exist in the table"+bcolors.ENDC)

    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'