# Weather Chatbot

A modular Python weather chatbot that answers questions using data from the Meteo API and OpenAI. The app supports queries on temperature comparisons, forecasts, wind conditions, and day length differences.

## Requirements

- **Python:** 3.9.16
- **Dependencies:**
A `requirements.txt` is provided. 

## Setup

1. **Create a Virtual Environment:**

   On Windows:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate

2. **Install Dependencies:**

    pip install -r requirements.txt

3. **Configure Environment:**

    Create a .env file in the project root with your OpenAI API key:
    OPENAI_API_KEY=your_openai_api_key_here

## Running the app

    python main.py

    Ask weather-related questions.