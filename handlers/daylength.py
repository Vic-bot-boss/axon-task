from datetime import date
from utils.weather_api import get_astronomy_data, compute_day_length
from config import DEFAULT_LAT, DEFAULT_LON, LOCATION_DESC

def get_shortest_day_date(today):
    """
    For a northern hemisphere location, returns the date of the winter solstice.
    If today is before December 21, use December 21 of last year; otherwise use December 21 of this year.
    """
    dec21_current = date(today.year, 12, 21)
    if today < dec21_current:
        return date(today.year - 1, 12, 21)
    else:
        return dec21_current

def compose_daylength_context(user_question):
    """
    Composes the data context for day length questions.
    Retrieves today's sunrise and sunset and that of the shortest day, computes day lengths,
    and appends the original question.
    """
    # Today's data
    today_date = date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_data = get_astronomy_data(today_str, DEFAULT_LAT, DEFAULT_LON)
    day_length_today = compute_day_length(today_data["sunrise"], today_data["sunset"])
    
    # Shortest day data
    shortest_date = get_shortest_day_date(today_date)
    shortest_str = shortest_date.strftime("%Y-%m-%d")
    shortest_data = get_astronomy_data(shortest_str, DEFAULT_LAT, DEFAULT_LON)
    day_length_shortest = compute_day_length(shortest_data["sunrise"], shortest_data["sunset"])
    
    # Compute difference (in seconds)
    difference = day_length_today - day_length_shortest
    
    # Format seconds into hours and minutes
    def format_seconds(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours} hours and {minutes} minutes"
    
    context = (
        f"Data Context:\n"
        f"- Location: {LOCATION_DESC}\n"
        f"- Today's date: {today_str}\n"
        f"   * Sunrise: {today_data['sunrise']}\n"
        f"   * Sunset: {today_data['sunset']}\n"
        f"   * Day length: {format_seconds(day_length_today)}\n"
        f"- Shortest day ({shortest_str}):\n"
        f"   * Sunrise: {shortest_data['sunrise']}\n"
        f"   * Sunset: {shortest_data['sunset']}\n"
        f"   * Day length: {format_seconds(day_length_shortest)}\n"
        f"- Difference: {format_seconds(difference)} longer daytime today than the shortest day.\n\n"
    )
    prompt = context + f"User Question: {user_question}"
    return prompt
