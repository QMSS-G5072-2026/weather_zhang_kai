# read version from installed package
from importlib.metadata import version
__version__ = version("weather_kz2635")
from .weather_kz2635 import celsius_to_fahrenheit, summarize_temperatures, clean_readings