from typing import Type, Callable, Optional
import json
import re


class Column:
    def __init__(self, ctype: Type, options=None, autosave_callback=None) -> None:
        if options is None:
            options = []
        self.Type: Type = ctype
        self.Data: list = []
        self.Options: list[str] = options
        self.Save = autosave_callback

    def __gt__(self, other) -> list:
        return [value > other for value in self.Data]

    def __lt__(self, other) -> list:
        return [value < other for value in self.Data]

    def __eq__(self, other) -> list:
        return [value == other for value in self.Data]

    def __ge__(self, other) -> list:
        return [value >= other for value in self.Data]

    def __le__(self, other) -> list:
        return [value <= other for value in self.Data]

    def __ne__(self, other) -> list:
        return [value != other for value in self.Data]

    def between(self, min_val, max_val) -> list:
        return [min_val < value < max_val for value in self.Data]

    def match(self, regex) -> list:
        return [re.match(regex, value) is not None for value in self.Data]

    def __len__(self) -> int:
        return len(self.Data)

    def Add(self, *values) -> None:
        for value in values:
            if not isinstance(value, self.Type) and value is not None:
                raise ValueError(f"Value {value} is not of type {self.Type}")
            self.Data.append(value)
        if self.Save != None:
            self.Save()

    def RemoveFirst(self) -> None:
        self.Data.pop(0)
        if self.Save != None:
            self.Save()

    def RemoveLast(self) -> None:
        self.Data.pop()
        if self.Save != None:
            self.Save()

    def RemoveAll(self, value) -> None:
        self.Data = [i for i in self.Data if i != value]
        if self.Save != None:
            self.Save()

    def RemoveAt(self, index) -> None:
        self.Data.pop(index)
        if self.Save != None:
            self.Save()

    def RemoveIf(self, func) -> None:
        self.Data = [i for i in self.Data if not func(i)]
        if self.Save != None:
            self.Save()

    def RemoveByList(self, values) -> None:
        self.Data = [self.Data[i] for i in range(len(self.Data)) if not values[i]]
        if self.Save != None:
            self.Save()

    def GetIf(self, func) -> list:
        return [i for i in self.Data if func(i)]

    def Get(self, index) -> Type:
        return self.Data[index]

    def Apply(self, func) -> None:
        self.Data = list(map(func, self.Data))
        if self.Save != None:
            self.Save()

    def ApplyIf(self, func, condition) -> None:
        self.Data = [func(i) if condition(i) else i for i in self.Data]
        if self.Save != None:
            self.Save()

    def ReType(self, newType: Type) -> None:
        try:
            self.Data = [newType(i) for i in self.Data]
            self.Type = newType
            if self.Save != None:
                self.Save()
        except Exception as e:
            raise ValueError(f"Cannot convert to {newType}: {e}")

    def isEmpty(self) -> bool:
        return len(self.Data) == 0

    def __str__(self) -> str:
        data = ""
        max_len = len(str(len(self.Data)))
        for i in range(len(self.Data)):
            data += f"{str(i).ljust(max_len)} | {self.Data[i]}\n"
        return f"Column {self.Type.__name__} with {len(self)} elements \n{data[:-1] if data else 'Empty'}"

    def toJson(self):
        return {"Type": self.Type.__name__, "Data": self.Data, "Options": self.Options}
