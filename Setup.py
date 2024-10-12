from setuptools import setup, find_packages
from pathlib import Path

# Reading the README file with UTF-8 encoding
this_directory = Path(__file__).parent
long_description = "Pilite is a lightweight database"

setup(
    name="Pylite",
    version="0.1.0",
    description="A lightweight database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ilify",
    packages=find_packages(),
)
