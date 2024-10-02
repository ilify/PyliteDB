class Column:
    def __init__(self, name):
        self.name = name
        self._operation = None
        self._value = None

    def __gt__(self, value):
        self._operation = ">"
        self._value = value
        return self

    def __eq__(self, value):
        self._operation = "=="
        self._value = value
        return self

    def evaluate(self, row):
        # Evaluate the stored condition for this column in the context of a given row
        if self._operation == ">":
            return row[self.name] > self._value
        elif self._operation == "==":
            return row[self.name] == self._value
        return False


class Table:
    def __init__(self, table_name):
        self.table_name = table_name
        self.rows = []
        self.columns = set()

    def Insert(self, **data):
        self.rows.append(data)
        self.columns.update(data.keys())

    def Select(self, columns=None, where=None):
        result = []
        for row in self.rows:
            if where is None or where.evaluate(row):
                if columns is None:
                    result.append(row)
                else:
                    result.append({col: row[col] for col in columns})
        return result

    def __getattr__(self, name):
        # Allow access to dynamic columns as attributes
        if name in self.columns:
            return Column(name)
        raise AttributeError(f"'Table' object has no attribute '{name}'")


# Usage example
t = Table("Employees")
t.Insert(Id=1, Name="John", Age=25, Salary=50000.0)
t.Insert(Id=2, Name="Jane", Age=22, Salary=45000.0)

# Select example using direct comparisons without needing to define columns upfront
result = t.Select(
    columns=["Name", "Age"],
    where=t.Age > 20  # Use columns directly
)

# `result` should contain rows where Age is greater than 20
print(result)  # Output: [{'Name': 'John', 'Age': 25}, {'Name': 'Jane', 'Age': 22}]
