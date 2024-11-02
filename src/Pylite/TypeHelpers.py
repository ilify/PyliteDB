import re
import faker
class email(str):
    def __new__(cls, value):
        if not re.match(r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", value, re.MULTILINE):
            raise ValueError("Invalid email")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().email()



class password(str):
    length = 8
    def __new__(cls, value):
        if len(value) < cls.length:
            raise ValueError(f"Password must be at least {cls.length} characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        fake = faker.Faker()
        return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

