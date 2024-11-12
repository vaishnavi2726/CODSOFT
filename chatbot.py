import re
import time
import urllib.request
import json
import math

# API Keys (Replace with your actual API keys from respective services)
WEATHER_API_KEY = "YOUR_WEATHER_API_KEY"  # Get from https://openweathermap.org/api
CURRENCY_API_KEY = "YOUR_CURRENCY_API_KEY"  # Get from https://exchangerate-api.com
NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Get from https://newsapi.org

# Step 1: Define patterns and responses with real-time capabilities
patterns_responses = {
    r"(hi|hello|hey|holla|greetings)": "Hello! How can I assist you today?",
    r"(how are you|how's it going|how are you doing)": "I'm just a bot, but I'm doing great! How about you?",
    r"(what is your name|who are you)": "I am a friendly chatbot created to assist you.",
    r"(what time is it|tell me the time)": f"The current time is {time.strftime('%H:%M:%S')}",
    r"(bye|goodbye|see you later)": "Goodbye! Have a great day!",
    r"(.*)": "I'm sorry, I didn't understand that. Could you please rephrase?",
    r"(weather in .*)": "Sure, let me get the weather for you.",
    r"(convert (.*) to (.*))": "Let me get the conversion for you.",
    r"(news|latest news)": "Sure, I can fetch the latest news for you.",
    r"(capital of .*)": "Let me find the capital of that state or country for you."
}

# Step 2: Define a dictionary for state/country capitals
state_capitals = {
    "alabama": "Montgomery",
    "alaska": "Juneau",
    "arizona": "Phoenix",
    "arkansas": "Little Rock",
    "california": "Sacramento",
    "colorado": "Denver",
    "connecticut": "Hartford",
    "delaware": "Dover",
    "florida": "Tallahassee",
    "georgia": "Atlanta",
    "hawaii": "Honolulu",
    "idaho": "Boise",
    "illinois": "Springfield",
    "indiana": "Indianapolis",
    "iowa": "Des Moines",
    "kansas": "Topeka",
    "kentucky": "Frankfort",
    "louisiana": "Baton Rouge",
    "maine": "Augusta",
    "maryland": "Annapolis",
    "massachusetts": "Boston",
    "michigan": "Lansing",
    "minnesota": "Saint Paul",
    "mississippi": "Jackson",
    "missouri": "Jefferson City",
    "montana": "Helena",
    "nebraska": "Lincoln",
    "nevada": "Carson City",
    "new hampshire": "Concord",
    "new jersey": "Trenton",
    "new mexico": "Santa Fe",
    "new york": "Albany",
    "north carolina": "Raleigh",
    "north dakota": "Bismarck",
    "ohio": "Columbus",
    "oklahoma": "Oklahoma City",
    "oregon": "Salem",
    "pennsylvania": "Harrisburg",
    "rhode island": "Providence",
    "south carolina": "Columbia",
    "south dakota": "Pierre",
    "tennessee": "Nashville",
    "texas": "Austin",
    "utah": "Salt Lake City",
    "vermont": "Montpelier",
    "virginia": "Richmond",
    "washington": "Olympia",
    "west virginia": "Charleston",
    "wisconsin": "Madison",
    "wyoming": "Cheyenne",
    "canada": "Ottawa",
    "mexico": "Mexico City",
    "france": "Paris",
    "germany": "Berlin",
    "italy": "Rome",
    "spain": "Madrid",
    "united kingdom": "London",
    "india": "New Delhi",
    "china": "Beijing",
    "japan": "Tokyo",
    "brazil": "Brasília"
}

# Step 3: Function to process user input and match patterns
def get_response(user_input):
    user_input = user_input.lower()  # Convert to lowercase for case-insensitive matching
    
    # Check for weather-related query
    if re.search(r"weather in (.*)", user_input):
        location = re.search(r"weather in (.*)", user_input).group(1)
        return get_weather(location)
    
    # Check for currency conversion query
    if re.search(r"convert (.*) to (.*)", user_input):
        currencies = re.findall(r"convert (.*) to (.*)", user_input)
        return convert_currency(currencies[0][0], currencies[0][1])

    # Check for news-related query
    if "news" in user_input:
        return get_news()
    
    # Check for capital-related query
    if re.search(r"capital of (.*)", user_input):
        state_or_country = re.search(r"capital of (.*)", user_input).group(1)
        return get_capital(state_or_country)

    # General response based on predefined patterns
    for pattern, response in patterns_responses.items():
        if re.search(pattern, user_input):  # If pattern matches user input
            return response
    return "I'm sorry, I didn't understand that."

# Step 4: Fetch Weather Data (OpenWeatherMap API) using urllib
def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if data['cod'] == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                city = data['name']
                return f"The current weather in {city} is {temp}°C with {description}."
            else:
                return "I couldn't find the weather for that location. Please check the name and try again."
    except Exception as e:
        return f"Error retrieving weather data: {e}"

# Step 5: Currency Conversion (ExchangeRate API) using urllib
def convert_currency(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{from_currency}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if data['result'] == "success":
                conversion_rate = data['conversion_rates'].get(to_currency.upper())
                if conversion_rate:
                    return f"1 {from_currency} is equal to {conversion_rate} {to_currency}."
                else:
                    return f"Sorry, I couldn't find conversion rates for {to_currency}."
            else:
                return "Error retrieving currency data. Please try again."
    except Exception as e:
        return f"Error retrieving currency data: {e}"

# Step 6: Fetch Latest News (NewsAPI) using urllib
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if data['status'] == 'ok':
                articles = data['articles'][:5]  # Get top 5 news articles
                news = "Here are the top news headlines:\n"
                for article in articles:
                    news += f"- {article['title']} ({article['source']['name']})\n"
                return news
            else:
                return "Sorry, I couldn't retrieve the news at the moment."
    except Exception as e:
        return f"Error retrieving news data: {e}"

# Step 7: Get the Capital of a State or Country
def get_capital(state_or_country):
    state_or_country = state_or_country.lower().strip()
    if state_or_country in state_capitals:
        return f"The capital of {state_or_country.title()} is {state_capitals[state_or_country]}."
    else:
        return f"Sorry, I don't have information about the capital of {state_or_country.title()}."

# Step 8: Main loop for chatting
def chatbot():
    print("Chatbot: Hello! How can I assist you today?")
    
    while True:
        user_input = input("You: ")  # Get user input
        if re.search(r"(bye|goodbye|see you later)", user_input.lower()):
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        response = get_response(user_input)  # Get response from the chatbot
        print(f"Chatbot: {response}")

# Start the chatbot
chatbot()