import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("Please set your OPENAI_API_KEY environment variable.")

# Default location: Copenhagen
DEFAULT_LAT = 55.6761
DEFAULT_LON = 12.5683
LOCATION_DESC = f"Copenhagen (lat: {DEFAULT_LAT}, lon: {DEFAULT_LON})"

# API endpoints for Open-Meteo
HISTORICAL_API_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
