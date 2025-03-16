from utils.weather_api import get_tomorrow_forecast_temp
from config import DEFAULT_LAT, DEFAULT_LON, LOCATION_DESC

def compose_forecast_context(user_question):
    """
    Composes the data context for forecast questions.
    Retrieves tomorrow's forecast data and appends the original question.
    """
    forecast_data = get_tomorrow_forecast_temp(lat=DEFAULT_LAT, lon=DEFAULT_LON)
    context = (
        f"Data Context:\n"
        f"- Location: {LOCATION_DESC}\n"
        f"- Forecast for {forecast_data['date']}:\n"
        f"   * Predicted min temperature: {forecast_data['tmin']}°C\n"
        f"   * Predicted max temperature: {forecast_data['tmax']}°C\n"
        f"   * Average temperature: {forecast_data['avg']:.2f}°C\n\n"
    )
    prompt = context + f"User Question: {user_question}"
    return prompt
