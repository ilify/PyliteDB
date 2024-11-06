# __init__.py
from .TypeHelpers import *
from .Table import Table
from .Database import Database

# from .DepColumn import Column
# from .Types import PyliteTypes

# Optional: Metadata
__version__ = "0.4.1"
__author__ = "Ilify"
__email__ = "iliesmraihia@gmail.com"

# Provide a simple package-level description
"""
PyLite: A lightweight database library using Pandas DataFrames.
"""

# Expose the Database class when the package is imported
__all__ = ["Database", "Table","email","password","color","phone","username","url","creditCard","date","currency","postalCode","uuid","latitude","longitude","location","ipv4","mac","path","domain"]
