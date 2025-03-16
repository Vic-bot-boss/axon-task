import requests
import statistics
from datetime import date, timedelta, datetime
from astral import LocationInfo
from astral.sun import sun
from config import HISTORICAL_API_URL, FORECAST_API_URL

def get_january_avg_temp(year, lat, lon):
    """
    Retrieves historical temperature data for January of the specified year and
    computes the monthly average temperature using daily min and max.
    """
    start_date = f"{year}-01-01"
    end_date = f"{year}-01-31"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_min,temperature_2m_max",
        "timezone": "auto"
    }
    response = requests.get(HISTORICAL_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    tmin = data["daily"]["temperature_2m_min"]
    tmax = data["daily"]["temperature_2m_max"]
    daily_averages = [(min_temp + max_temp) / 2 for min_temp, max_temp in zip(tmin, tmax)]
    return statistics.mean(daily_averages)

def get_tomorrow_forecast_temp(lat, lon):
    """
    Retrieves forecast temperature data for tomorrow using the forecast API.
    Returns a dictionary with tomorrow's date, min, max, and average temperature.
    """
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_min,temperature_2m_max",
        "start_date": tomorrow_str,
        "end_date": tomorrow_str,
        "timezone": "auto"
    }
    response = requests.get(FORECAST_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    tmin = data["daily"]["temperature_2m_min"][0]
    tmax = data["daily"]["temperature_2m_max"][0]
    avg_temp = (tmin + tmax) / 2
    return {"date": tomorrow_str, "tmin": tmin, "tmax": tmax, "avg": avg_temp}

def get_today_wind_forecast(lat, lon):
    """
    Retrieves today's wind forecast using the forecast API.
    Returns a dictionary with today's date and the maximum wind speed.
    """
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "windspeed_10m_max",
        "start_date": today_str,
        "end_date": today_str,
        "timezone": "auto"
    }
    response = requests.get(FORECAST_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    try:
        wind_today = data["daily"]["windspeed_10m_max"][0]
    except (KeyError, IndexError):
        raise Exception("Wind forecast data not found in API response")
    return {"date": today_str, "windspeed": wind_today}

def get_historical_wind_speed(year, month, day, lat, lon):
    """
    Retrieves historical wind data for a specific day (given by year, month, day)
    using the historical API.
    Returns a dictionary with the date and maximum wind speed.
    """
    date_str = f"{year}-{month:02d}-{day:02d}"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_str,
        "end_date": date_str,
        "daily": "windspeed_10m_max",
        "timezone": "auto"
    }
    response = requests.get(HISTORICAL_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    try:
        wind_hist = data["daily"]["windspeed_10m_max"][0]
    except (KeyError, IndexError):
        raise Exception("Historical wind data not found in API response")
    return {"date": date_str, "windspeed": wind_hist}

def get_astronomy_data(date_str, lat, lon):
    """
    Computes sunrise and sunset times for the given date and location using the astral library.
    The date_str is in "YYYY-MM-DD" format.
    """
    # You can set the name and region as desired. Here we use Copenhagen as default.
    location = LocationInfo(name="Copenhagen", region="Denmark", timezone="Europe/Copenhagen", latitude=lat, longitude=lon)
    target_date = datetime.fromisoformat(date_str).date()
    s = sun(location.observer, date=target_date, tzinfo=location.timezone)
    # Return ISO formatted strings.
    return {"sunrise": s["sunrise"].isoformat(), "sunset": s["sunset"].isoformat()}

def compute_day_length(sunrise, sunset):
    """
    Computes the day length in seconds given sunrise and sunset ISO timestamps.
    """
    sunrise_dt = datetime.fromisoformat(sunrise)
    sunset_dt = datetime.fromisoformat(sunset)
    return (sunset_dt - sunrise_dt).total_seconds()
