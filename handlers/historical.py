from utils.weather_api import get_january_avg_temp
from config import DEFAULT_LAT, DEFAULT_LON, LOCATION_DESC

def compose_historical_context(user_question):
    """
    Composes the data context for historical temperature questions.
    Retrieves January data for 2025 and 2024, then appends the original question.
    """
    current_year = 2025
    previous_year = 2024
    temp_current = get_january_avg_temp(current_year, lat=DEFAULT_LAT, lon=DEFAULT_LON)
    temp_previous = get_january_avg_temp(previous_year, lat=DEFAULT_LAT, lon=DEFAULT_LON)
    context = (
        f"Data Context:\n"
        f"- Location: {LOCATION_DESC}\n"
        f"- January {current_year} average temperature: {temp_current:.2f}°C\n"
        f"- January {previous_year} average temperature: {temp_previous:.2f}°C\n\n"
    )
    prompt = context + f"User Question: {user_question}"
    return prompt
