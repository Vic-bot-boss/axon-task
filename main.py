from utils.openai_helper import ask_llm, classify_question
from handlers.historical import compose_historical_context
from handlers.forecast import compose_forecast_context
from handlers.wind import compose_wind_context
from handlers.daylength import compose_daylength_context

# Registry mapping intents to context composer functions.
intent_registry = {
    "historical": compose_historical_context,
    "forecast": compose_forecast_context,
    "wind": compose_wind_context,
    "daylength": compose_daylength_context
}

def handle_question(user_question):
    """
    Routes the user's question based on its classified intent.
    The original question is passed to the context composer.
    """
    intent = classify_question(user_question)
    if intent in intent_registry:
        prompt = intent_registry[intent](user_question)
        return ask_llm(prompt)
    else:
        return "Sorry, I cannot answer that question yet. Try asking about January temperatures, tomorrow's weather, wind conditions, or day length."

def main():
    print("Welcome to the Weather Chatbot!")
    print("Examples:")
    print("  - 'Is the temperature this January higher than last year?'")
    print("  - 'Is it cold in Copenhagen tomorrow?'")
    print("  - 'It feels windy today in Copenhagen. Is this common for this time of year?'")
    print("  - 'How much longer is daytime (sunrise to sunset) today than the shortest day of the year in my location?'\n")
    
    while True:
        user_question = input("Enter your weather question (or type 'exit' to quit): ")
        if user_question.strip().lower() == "exit":
            break
        answer = handle_question(user_question)
        print("\nLLM Answer:")
        print(answer)
        print("\n---\n")

if __name__ == "__main__":
    main()
