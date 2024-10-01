# PyLite

**Pylite** is a lightweight, Python-based database library , It allows for efficient data manipulation and querying while maintaining simplicity and ease of use. Designed for small to medium-sized projects.

## Features

- **Lightweight and Simple**: Minimal setup and configuration needed.

## Usage

# Column Class

## Methods

# Column Class Methods

| Method                    | Description                                                                                                                                                      |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__init__(ctype)`         | Initializes a new `Column` instance with the specified type `ctype`.                                                                                             |
| `Add(value)`              | Adds a single value of the correct type to the column.                                                                                                           |
| `AddAll(*values)`         | Adds multiple values at once to the column.                                                                                                                      |
| `__getitem__(condition)`  | Retrieves values based on the provided index or a list of boolean conditions.                                                                                    |
| `Get(index)`              | Returns the value at the specified index.                                                                                                                        |
| `__setitem__(key, value)` | Sets a value at a specific index or based on a list of booleans.                                                                                                 |
| `RemoveFirst()`           | Removes the first element from the column.                                                                                                                       |
| `RemoveLast()`            | Removes the last element from the column.                                                                                                                        |
| `RemoveAll(value)`        | Removes all occurrences of the specified value from the column.                                                                                                  |
| `RemoveAt(index)`         | Removes the element at the specified index.                                                                                                                      |
| `Removeif(func)`          | Removes elements that satisfy the condition defined in the provided function.                                                                                    |
| `Getif(func)`             | Retrieves all elements that satisfy the condition defined in the provided function.                                                                              |
| `between(start, end)`     | Checks which values are within the specified range (inclusive).                                                                                                  |
| `Apply(func)`             | Applies a function to each element in the column.                                                                                                                |
| `__len__()`               | Returns the number of elements in the column.                                                                                                                    |
| `__str__()`               | Provides a string representation of the column, including its type and elements.                                                                                 |
| `__gt__(threshold)`       | Compares each element to the specified threshold and returns a list of boolean values indicating whether each element is greater than the threshold.             |
| `__lt__(threshold)`       | Compares each element to the specified threshold and returns a list of boolean values indicating whether each element is less than the threshold.                |
| `__ge__(threshold)`       | Compares each element to the specified threshold and returns a list of boolean values indicating whether each element is greater than or equal to the threshold. |
| `__le__(threshold)`       | Compares each element to the specified threshold and returns a list of boolean values indicating whether each element is less than or equal to the threshold.    |
| `__eq__(threshold)`       | Compares each element to the specified threshold and returns a list of boolean values indicating whether each element is equal to the threshold.                 |
| `__ne__(threshold)`       | Compares each element to the specified threshold and returns a list of boolean values indicating whether each element is not equal to the threshold.             |
| `__contains__(values)`    | Checks if the specified value exists in the column and returns a boolean result.                                                                                 |

## Import

To use the `Column` class, simply copy the `Column` class code into your project.

```python
from column import Column
```
