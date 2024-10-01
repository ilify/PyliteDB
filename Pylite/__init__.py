# __init__.py

from .pyTable import Table 
from .pyDatabase import Database 
from .pyColumn import Column

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
