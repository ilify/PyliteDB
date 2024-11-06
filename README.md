# Pylite Database

Pylite is a lightweight database system built in Python. It provides a simple and intuitive interface for creating, managing, and querying data with support for table relationships, type validation, and event handling.

## Features

- 🔒 **Built-in Encryption**: Secure your data with AES-GCM encryption
- 📊 **Pandas Integration**: Powered by pandas DataFrame for efficient data manipulation
- 🔗 **Table Relationships**: Support for primary and foreign key relationships
- 🎯 **Type Validation**: Built-in type checking and custom type validators
- 🎭 **Event System**: Comprehensive event hooks for database operations
- 💾 **Auto-save Capability**: Optional automatic saving after modifications
- 🔄 **SQL Import**: Import existing SQLite databases
- 📝 **Custom Types**: Includes email and password validators with fake data generation

## Installation

```bash
pip install PyliteDB  # Package name may vary
```

## Quick Start

```python
from pylite import Database, email, password

# Create a new database
db = Database(AutoSave=True)

# Create a users table with typed columns
db.CreateTable("Users").AddColumn(
    ID=int,
    Email=email,
    Password=password,
    Username=str
)

# Insert data
db.Users.Insert(
    ID=1,
    Email="user@example.com",
    Password="SecurePass123!",
    Username="john_doe"
)

# Save database with encryption
db.Save("my_database.pylite", "your_secure_password")

# Load existing database
db = Database("my_database.pylite", "your_secure_password")
```

## Working with Tables

### Creating Tables

```python
# Create table with columns
db.CreateTable("Products").AddColumn(
    ID=int,
    Name=str,
    Price=float,
    Stock=int
)
```

### CRUD Operations

```python
# Insert
db.Products.Insert(ID=1, Name="Widget", Price=9.99, Stock=100)

# Select
product = db.Products.Get(ID=1)
filtered = db.Products.Select(db.Products.Price > 5.00)

# Update
db.Products.Update(db.Products.ID == 1, Price=10.99)
db.Products.UpdateAt(0, Stock=95)

# Delete
db.Products.Delete(db.Products.Stock == 0)
db.Products.DeleteAt(0)
```

### Table Relationships

```python
# Create related tables
db.CreateTable("Orders").AddColumn(
    OrderID=int,
    ProductID=int,
    Quantity=int
)

# Link tables
db.Link(db.Orders.ProductID, db.Products.ID)
```

## Event Handling

```python
# Add event handlers
db.Users.afterInsert = lambda table, added: print(f"New user added: {added['Username']}")
db.Users.beforeDelete = lambda table: print("About to delete user(s)")
```

## Custom Types

Pylite includes built-in custom types with validation:

### Email Type

```python
# Validates email format
db.CreateTable("Contacts").AddColumn(
    Email=email  # Ensures valid email format
)
```

### Password Type

```python
# Enforces password requirements
db.CreateTable("Accounts").AddColumn(
    Password=password  # Requires length, upper/lower case, numbers, special chars
)
```

## Data Security

Pylite uses AES-GCM encryption with:

- PBKDF2 key derivation
- Random salt generation
- Secure IV handling
- Authentication tags

```python
# Save with encryption
db.Save("secure_database.pylite", "your_strong_password")

# Load encrypted database
db = Database("secure_database.pylite", "your_strong_password")
```

## Method Reference

### Database Class Methods

#### Core Database Operations

```python
Database(Path="", Password="", AutoSave=False)  # Constructor
Database.Save(Path="", Password="", asJson=False)  # Save database to file
Database.Load()  # Load database from file
Database.LoadFromSQL(SQLFilePath)  # Load from SQLite database
Database.ChangePassword(Password)  # Change database encryption password
```

#### Table Management

```python
Database.CreateTable(TableName)  # Create new table
Database.DeleteTable(TableName)  # Delete existing table
Database.RenameTable(OldName, NewName)  # Rename table
Database.GetTables()  # Get list of all tables
Database.ClearEmptyTables()  # Remove all empty tables
Database.Link(source, target)  # Create relationship between tables
```

### Table Class Methods

#### Column Operations

```python
Table.AddColumn(**columns)  # Add new columns with types
Table.RemoveColumn(ColumnName)  # Remove column
Table.RenameColumn(OldName, NewName)  # Rename column
Table.ReorderColumns(NewOrder)  # Reorder columns
```

#### CRUD Operations

```python
# Create
Table.Insert(**columns)  # Insert new row

# Read
Table.Select(condition=None)  # Select rows matching condition
Table.Get(**columns)  # Get first row matching conditions
Table[column_name]  # Access column data
Table[row_index]  # Access row data

# Update
Table.Update(selector=None, **columns)  # Update rows matching selector
Table.UpdateAt(index, **columns)  # Update row at specific index

# Delete
Table.Delete(condition=None, index=None, all=False)  # Delete rows
Table.DeleteAt(index)  # Delete row at specific index
```

#### Query Operations

```python
Table.Sort(Column, ascending=True)  # Sort table by column
Table.Limit(n)  # Limit to first n rows
Table.RemoveDuplicates()  # Remove duplicate rows
Table.Exists(**columns)  # Check if rows matching conditions exist
```

#### Data Analysis

```python
Table.ColumnStats(column)  # Get column statistics
Table.Difference(OtherTable)  # Compare with another table
Table.Intersection(OtherTable, onColumn=None)  # Get common rows
Table.Union(OtherTable)  # Combine tables
Table.Distinct(Column)  # Get unique values in column
Table.Map(Column, Mapping)  # Apply mapping to column
```

#### Properties and Attributes

```python
Table.Columns  # List of column names
Table.Rows  # List of all rows
Table.Length  # Number of rows
Table.df  # Access underlying pandas DataFrame
len(table)  # Get number of rows
```

#### Storage Operations

```python
Table.SaveToDisk(path)  # Save single table to file
Table.LoadFromDisk(path)  # Load single table from file
Table.toDict()  # Convert table to dictionary
Table.loadFromDict(data)  # Load table from dictionary
```

#### Event Handlers

Tables support the following event hooks:

- `beforeInsert`, `afterInsert`
- `beforeUpdate`, `afterUpdate`
- `beforeDelete`, `afterDelete`
- `beforeRenameColumn`, `afterRenameColumn`
- `beforeRemoveColumn`, `afterRemoveColumn`
- `beforeSelect`, `afterSelect`
- `beforeAddColumn`, `afterAddColumn`
- `beforeCopy`, `afterCopy`

```python
# Example of event handler usage
table.afterInsert = lambda table, added: print(f"Added new row: {added}")
```

## Additional Features

- **Auto-save**: Enable automatic saving after modifications
- **SQL Import**: Import existing SQLite databases
- **Table Operations**: Sort, filter, limit, and manipulate data
- **Data Statistics**: Get column statistics and table information
- **Data Export**: Convert tables to dictionaries or save individually

## Best Practices

1. **Always use strong passwords** for database encryption
2. **Enable AutoSave** for important data
3. **Implement event handlers** for critical operations
4. **Use appropriate column types** for data validation
5. **Regular backups** of database files

## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or suggest improvements.

## License

[MIT License](LICENSE)

## Support

For support, please open an issue on the GitHub repository or contact the maintainers.
