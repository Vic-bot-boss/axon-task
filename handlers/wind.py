from datetime import date
from utils.weather_api import get_today_wind_forecast, get_historical_wind_speed
from config import DEFAULT_LAT, DEFAULT_LON, LOCATION_DESC

def compose_wind_context(user_question):
    """
    Composes the data context for wind questions.
    Retrieves today's forecasted wind speed and historical wind speed
    for the same day last year, then appends the original question.
    """
    today = date.today()
    historical_year = today.year - 1
    forecast_data = get_today_wind_forecast(lat=DEFAULT_LAT, lon=DEFAULT_LON)
    historical_data = get_historical_wind_speed(historical_year, today.month, today.day, lat=DEFAULT_LAT, lon=DEFAULT_LON)
    
    context = (
        f"Data Context:\n"
        f"- Location: {LOCATION_DESC}\n"
        f"- Today's wind forecast ({forecast_data['date']}): Maximum wind speed: {forecast_data['windspeed']} km/h\n"
        f"- Historical wind data on {historical_data['date']}: Maximum wind speed: {historical_data['windspeed']} km/h\n\n"
    )
    prompt = context + f"User Question: {user_question}"
    return prompt
