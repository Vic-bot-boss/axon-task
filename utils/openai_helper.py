import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def ask_llm(prompt):
    """
    Sends the prompt to the LLM (using OpenAI's ChatCompletion) and returns the answer.
    """
    client = openai.OpenAI()  # Use the new OpenAI client

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers weather-related questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content.strip()
    return answer

def classify_question(user_question):
    """
    Uses the LLM to classify the user's question into an intent category.
    Returns "historical", "forecast", "wind", "daylength", or "unsupported".
    """
    prompt = f"""
You are a weather question classifier. Given a user's question, classify it into one of these categories:
- "historical": if the question asks about comparing historical temperature data (e.g. January comparisons).
- "forecast": if the question asks about tomorrow's weather forecast (temperature, precipitation, etc.).
- "wind": if the question asks about wind conditions (e.g. "It feels windy today...").
- "daylength": if the question asks about comparing today's daytime length (sunrise to sunset) to the shortest day of the year.
- "unsupported": if it doesn't match the above categories.

User's question: "{user_question}"

Answer with one word only.
"""
    classification = ask_llm(prompt).strip().lower()
    if "historical" in classification:
        return "historical"
    elif "forecast" in classification:
        return "forecast"
    elif "wind" in classification:
        return "wind"
    elif "daylength" in classification:
        return "daylength"
    else:
        return "unsupported"