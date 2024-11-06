from random import randint
import re
import faker
import colorsys
import uuid
from datetime import datetime
from typing import Tuple, Union
from decimal import Decimal
import math

from pycountry import currencies

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
        passwordPattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$'
        if not re.match(passwordPattern, value):
            raise ValueError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        import random
        fake = faker.Faker()
        return fake.password(length=randint(8,12), digits=True, upper_case=True, lower_case=True)

class color:
    def __init__(self, value: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]):
        if isinstance(value, str):
            if value.startswith('#'):
                self._from_hex(value)
            elif value.startswith('rgb'):
                self._from_rgb_string(value)
            elif value.startswith('hsl'):
                self._from_hsl_string(value)
            else:
                raise ValueError("Invalid color format")
        elif isinstance(value, tuple):
            if len(value) in (3, 4):
                self.r, self.g, self.b = value[:3]
                self.a = value[3] if len(value) == 4 else 255
            else:
                raise ValueError("Tuple must have 3 or 4 values (RGB or RGBA)")
        
        self._validate_values()

    def _validate_values(self):
        for val in (self.r, self.g, self.b, self.a):
            if not 0 <= val <= 255:
                raise ValueError("Color values must be between 0 and 255")

    def _from_hex(self, hex_str: str):
        hex_str = hex_str.lstrip('#')
        if len(hex_str) in (6, 8):
            self.r = int(hex_str[0:2], 16)
            self.g = int(hex_str[2:4], 16)
            self.b = int(hex_str[4:6], 16)
            self.a = int(hex_str[6:8], 16) if len(hex_str) == 8 else 255
        else:
            raise ValueError("Invalid hex color format")

    def _from_rgb_string(self, rgb_str: str):
        match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', rgb_str)
        if match:
            self.r = int(match.group(1))
            self.g = int(match.group(2))
            self.b = int(match.group(3))
            self.a = int(float(match.group(4)) * 255) if match.group(4) else 255
        else:
            raise ValueError("Invalid RGB(A) string format")

    def _from_hsl_string(self, hsl_str: str):
        match = re.match(r'hsla?\((\d+),\s*(\d+)%,\s*(\d+)%(?:,\s*([\d.]+))?\)', hsl_str)
        if match:
            h = int(match.group(1)) / 360
            s = int(match.group(2)) / 100
            l = int(match.group(3)) / 100
            rgb = colorsys.hls_to_rgb(h, l, s)
            self.r = int(rgb[0] * 255)
            self.g = int(rgb[1] * 255)
            self.b = int(rgb[2] * 255)
            self.a = int(float(match.group(4)) * 255) if match.group(4) else 255
        else:
            raise ValueError("Invalid HSL(A) string format")

    def to_hex(self, include_alpha: bool = False) -> str:
        if include_alpha:
            return f'#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}'
        return f'#{self.r:02x}{self.g:02x}{self.b:02x}'

    def to_rgb(self, include_alpha: bool = False) -> str:
        if include_alpha:
            return f'rgba({self.r}, {self.g}, {self.b}, {self.a/255:.2f})'
        return f'rgb({self.r}, {self.g}, {self.b})'

    def to_hsl(self, include_alpha: bool = False) -> str:
        h, l, s = colorsys.rgb_to_hls(self.r/255, self.g/255, self.b/255)
        if include_alpha:
            return f'hsla({int(h*360)}, {int(s*100)}%, {int(l*100)}%, {self.a/255:.2f})'
        return f'hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)'

    def to_tuple(self, include_alpha: bool = False) -> tuple:
        if include_alpha:
            return (self.r, self.g, self.b, self.a)
        return (self.r, self.g, self.b)

    def __repr__(self):
        return self.to_hex(True)

    __str__ = __repr__

    @staticmethod
    def fake():
        fake = faker.Faker()
        return color(f'#{fake.hex_color()[1:]}')

class phone(str):
    def __new__(cls, value):
        clean_number = re.sub(r'\D', '', value)
        if not (10 <= len(clean_number) <= 15):
            raise ValueError("Phone number must be between 10 and 15 digits")
        if not clean_number.isdigit():
            raise ValueError("Phone number can only contain digits")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().phone_number()

class username(str):
    def __new__(cls, value):
        if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", value):
            raise ValueError("Username must be 3-20 characters and contain only letters, numbers, underscores, and hyphens")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().user_name()

class url(str):
    def __new__(cls, value):
        if not re.match(
            r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$",
            value
        ):
            raise ValueError("Invalid URL format")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().url()

class creditCard(str):
    def __new__(cls, value):
        clean_number = re.sub(r'[\s-]', '', value)
        
        if not clean_number.isdigit():
            raise ValueError("Credit card number can only contain digits")
        
        def luhn_check(number):
            digits = [int(d) for d in number]
            checksum = 0
            for i in range(len(digits)-1, -1, -1):
                d = digits[i]
                if i % 2 == len(digits) % 2:
                    d *= 2
                    if d > 9:
                        d -= 9
                checksum += d
            return checksum % 10 == 0
        
        if not luhn_check(clean_number):
            raise ValueError("Invalid credit card number (failed Luhn check)")
        
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().credit_card_number()

class date(str):
    def __new__(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().date()

class currency(str):
    currencies = [
        "USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
        "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "INR", "RUB", "BRL", "ZAR",
        "PHP", "CZK", "PLN", "THB", "MYR", "IDR", "HUF", "AED", "SAR", "EGP",
        "ARS", "COP", "CLP", "PEN", "PKR", "VND", "BGN", "RON", "NGN", "UAH"
    ]

    def __new__(cls, value):
        if value not in currencies:
            raise ValueError("Invalid currency format")
        return super().__new__(cls, value)

    @staticmethod
    def fake():
        from random import choice
        currency_code = choice(currency.currencies)
        return currency_code
    
# class postalCode(str):
#     def __new__(cls, value):
#         patterns = {
#             'US': r'^\d{5}(-\d{4})?$',
#             'UK': r'^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$',
#             'CA': r'^[A-Z]\d[A-Z] ?\d[A-Z]\d$',
#         }
        
#         if not any(re.match(pattern, value.upper()) for pattern in patterns.values()):
#             raise ValueError("Invalid postal code format")
            
#         return super().__new__(cls, value)
    
#     @staticmethod
#     def fake():
#         return faker.Faker().postcode()

class uuid(str):
    def __new__(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("Invalid UUID format")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return str(uuid.uuid4())

class latitude(float):
    def __new__(cls, value):
        try:
            float_val = float(value)
            if not -90 <= float_val <= 90:
                raise ValueError("Latitude must be between -90 and 90 degrees")
        except ValueError:
            raise ValueError("Invalid latitude value")
        return super().__new__(cls, float_val)
    
    @staticmethod
    def fake():
        return round(faker.Faker().latitude(), 6)

class longitude(float):
    def __new__(cls, value):
        try:
            float_val = float(value)
            if not -180 <= float_val <= 180:
                raise ValueError("Longitude must be between -180 and 180 degrees")
        except ValueError:
            raise ValueError("Invalid longitude value")
        return super().__new__(cls, float_val)
    
    @staticmethod
    def fake():
        return round(faker.Faker().longitude(), 6)

class location(Tuple[float, float]):
    """
    A class representing a geographic location with latitude and longitude coordinates.
    Includes validation, formatting, and distance calculation capabilities.
    """

    def __new__(cls, lat: Union[float, str, Tuple[float, float]], lon: Union[float, str] = None):
        # If a tuple is passed as the first argument, unpack it
        if isinstance(lat, tuple) and lon is None:
            lat, lon = lat
        # Convert lat and lon to latitude and longitude types for validation
        lat = latitude(lat)
        lon = longitude(lon)
        return super().__new__(cls, (lat, lon))

    @property
    def lat(self) -> float:
        return self[0]

    @property
    def lon(self) -> float:
        return self[1]

    
    def to_tuple(self) -> tuple:
        """Return location as dictionary with 'lat' and 'lon' keys."""
        return (float(self.lat),float(self.lon))
    
    def __repr__(self) -> str:
        return f"({self.lat}, {self.lon})"
    __str__ = __repr__


    def to_dms(self) -> Tuple[str, str]:
        """Convert to degrees, minutes, seconds format."""
        def decimal_to_dms(decimal: float, is_latitude: bool) -> str:
            direction = 'N' if decimal >= 0 and is_latitude else 'S' if is_latitude else 'E' if decimal >= 0 else 'W'
            decimal = abs(decimal)
            degrees = int(decimal)
            decimal_minutes = (decimal - degrees) * 60
            minutes = int(decimal_minutes)
            seconds = round((decimal_minutes - minutes) * 60, 2)
            return f"{degrees}°{minutes}'{seconds}\"{direction}"
            
        return (
            decimal_to_dms(float(self.lat), True),
            decimal_to_dms(float(self.lon), False)
        )
    
    def distance_to(self, other: 'location', unit: str = 'km') -> float:
        """
        Calculate distance to another location using the Haversine formula.
        
        Args:
            other: Another location object
            unit: Distance unit ('km' for kilometers, 'mi' for miles, 'nm' for nautical miles)
            
        Returns:
            Distance in specified unit
        """
        R = {'km': 6371, 'mi': 3959, 'nm': 3440}
        
        if unit not in R:
            raise ValueError("Unit must be 'km', 'mi', or 'nm'")
            
        lat1, lon1 = math.radians(float(self.lat)), math.radians(float(self.lon))
        lat2, lon2 = math.radians(float(other.lat)), math.radians(float(other.lon))
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return round(R[unit] * c, 2)
    
    def is_in_bounds(self, bounds: Tuple[float, float, float, float]) -> bool:
        """
        Check if location is within given bounds.
        
        Args:
            bounds: Tuple of (min_lat, max_lat, min_lon, max_lon)
            
        Returns:
            bool: True if location is within bounds
        """
        min_lat, max_lat, min_lon, max_lon = bounds
        return (min_lat <= float(self.lat) <= max_lat and 
                min_lon <= float(self.lon) <= max_lon)
    
    @staticmethod
    def fake(bounds: Tuple[float, float, float, float] = None) -> 'location':
        """
        Generate a fake location, optionally within given bounds.
        
        Args:
            bounds: Optional tuple of (min_lat, max_lat, min_lon, max_lon)
            
        Returns:
            location: A new random location
        """
        fake = faker.Faker()
        if bounds:
            min_lat, max_lat, min_lon, max_lon = bounds
            lat = fake.random.uniform(min_lat, max_lat)
            lon = fake.random.uniform(min_lon, max_lon)
        else:
            lat = latitude.fake()
            lon = longitude.fake()
        return location(lat, lon)

class path(str):
    def __new__(cls, value):
        if not re.match(r'^(?:[a-zA-Z]:\\|/)(?:[^<>:"/\\|?*\n\r]+[/\\])*[^<>:"/\\|?*\n\r]*$', value):
            raise ValueError("Invalid file path format")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        fake = faker.Faker()
        extensions = ['.txt', '.pdf', '.doc', '.jpg', '.png']
        return f"{fake.file_path(depth=2, extension=fake.random.choice(extensions))}"

class mac(str):
    def __new__(cls, value):
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', value):
            raise ValueError("Invalid MAC address format")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().mac_address()

class domain(str):
    def __new__(cls, value):
        if not re.match(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid domain name format")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().domain_name()

class ipv4(str):
    def __new__(cls, value):
        if not re.match(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            value
        ):
            raise ValueError("Invalid IPv4 address")
        return super().__new__(cls, value)
    
    @staticmethod
    def fake():
        return faker.Faker().ipv4()