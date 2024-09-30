from setuptools import setup, find_packages
from pathlib import Path

# Reading the README file with UTF-8 encoding
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="Pylite",
    version="0.1.0",
    description="A lightweight database library using Pandas DataFrames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ilify",
    packages=find_packages(),
    install_requires=[
        "pandas"
    ],
)
