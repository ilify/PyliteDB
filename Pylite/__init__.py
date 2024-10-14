# __init__.py

from .Table import Table 
from .Database import Database 
from .Column import Column
from .Types import PyliteTypes

# Optional: Metadata
__version__ = "0.1.0"
__author__ = "Ilify"
__email__ = "iliesmraihia@gmail.com"

# Provide a simple package-level description
"""
PyLite: A lightweight database library using Pandas DataFrames.
"""

# Expose the Database class when the package is imported
__all__ = ['Database']
