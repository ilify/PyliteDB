# 🚀 **PyLite**

**PyLite** is a **lightweight database** built in Python 🐍, designed to be **super easy to use**, beginner-friendly 🎓, and **production-ready**! With **PyLite**, you can seamlessly perform essential database operations like **Insert**, **Select**, **Update**, and **Delete** using intuitive, Pythonic syntax. Perfect for both **learning** 📚 and **real-world** projects 🏗️!

### 💡 **Why Choose PyLite?**
- ❌ **0 Extra Code**
- ❌ **0 Complex Configurations**
- 🔄 **Built-in Converter** from SQL databases (using `sqlite3`)
- ⚙️ **1 Config File** to get started in no time
- 🧠 **Tightly Integrated** with Python
- 🌐 **Built-in DataBrowser** (Web-based) — use it **Standalone** or **Host** it!

## 🚀 **Getting Started**
#### ⚙️ Instalation


```bash
pip install git+https://github.com/ilify/Pylite.git
```

## 📚 Usage Without Config File

* Converting SQL to PYLITE Database
```python
from Pylite import Database
db = Database()
db.LoadFromSQL("SLQ_FILE_PATH")
db.Save("SAVE_LOCATION","YOUR_PASSWORD")
```

* Loading Database
```python
from Pylite import Database
db = Database("SAVE_LOCATION","YOUR_PASSWORD",AutoSave=True)
```

## 📚 Usage With Config File
Config Files are just python scripts to iniialize the database and create Tables shortcuts and more ...


Create a Config file `Database.py`


```python
from Pylite import Database

password = "YOUR_PASSWORD"
path     = "PYLITE_FILE_PATH" 
Database = Database(Path=path,Password=password,AutoSave=True)
# Table Shortcuts (Optional)
Accounts = Database.Accounts #Examples
```

Now Go to the script you Want to use pylite in for example `app.py`

```python
from Database import Accounts #Import Tables Directly

#Example Functions
def Login(Email,Password):
    return Accounts.Exists(
        Email    = Email ,
        Password = Password
    )

def SignUp(Email,Password):
    return Accounts.Insert(
        Email    = Email ,
        Password = Password
    )
```

