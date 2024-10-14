from Pylite.pyTypes import email
from Pylite.pyTypes import image
from Pylite.pyTypes import blob 


class PyliteTypes():
    SupportedTypes = [
            int,float, # Numeric
            str,email, # String
            bool, # Boolean
            list, # List
            dict, # Dictionary
            image, # Image
            blob,
    ]