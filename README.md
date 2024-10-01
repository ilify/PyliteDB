# PyLite

**Pylite** is a lightweight, Python-based database library , It allows for efficient data manipulation and querying while maintaining simplicity and ease of use. Designed for small to medium-sized projects.

## Features

- **Lightweight and Simple**: Minimal setup and configuration needed.

## Usage

# Column

<details>
<summary>Methods</summary>

| Method                   | Description                                                                                                                                              |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Add(value)`             | Adds a single value of the correct type to the column.                                                                                                   |
| `AddAll(*values)`        | Adds multiple values at once to the column.                                                                                                              |
| `Get(index)`             | Returns the value at the specified index.                                                                                                                |
| `RemoveFirst()`          | Removes the first element from the column.                                                                                                               |
| `RemoveLast()`           | Removes the last element from the column.                                                                                                             |
| `RemoveAll(value)`       | Removes all occurrences of the specified value from the column.                                                                                        |
| `RemoveAt(index)`        | Removes the element at the specified index.                                                                                                           |
| `Removeif(func)`         | Removes elements that satisfy the condition defined in the provided function.                                                                          |
| `Getif(func)`            | Retrieves all elements that satisfy the condition defined in the provided function.                                                                    |
| `between(start, end)`    | Checks which values are within the specified range (inclusive).                                                                                      |
| `Apply(func)`            | Applies a function to each element in the column.                                                                                                      |

</details>
