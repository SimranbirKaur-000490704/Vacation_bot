import openai
import csv
from flask import Flask, render_template, request, redirect, url_for
import os

# Initialize Flask app
app = Flask(__name__, static_folder='templates')

# Function to get completion from OpenAI
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1, # Degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Function to get completion from messages
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Function to collect messages
def collect_messages():
    if request.method == 'POST' and 'user_input' in request.form:
        prompt = request.form['user_input']
        context.append({'role': 'user', 'content': f"{prompt}"})
        response = get_completion_from_messages(context) 
        context.append({'role': 'assistant', 'content': f"{response}"})
        return redirect(url_for('index'))  # Redirect to GET request after processing POST
    return render_template('index.html', context=[msg for msg in context if msg['role'] != 'system'])

# Function to read data from CSV files
def read_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Read data from CSV files
cities = read_csv('csv_files/cities.csv')
flight_prices = read_csv('csv_files/flight_prices.csv')
hotel_options = read_csv('csv_files/hotel_options.csv')
sightseeing_packages = read_csv('csv_files/sightseeing_packages.csv')
sightseeing_prices = read_csv('csv_files/sightseeing_prices.csv')

# Initialize context with the first message from the assistant
context = [{'role':'system', 'content':"""
    You're VacayBot, a smart vacation booking assistant with emojis. \
    You greet the customer and help them select their destination for vacation. \
    If customer mentions a country name, check if that country has any city from exploration below. \
    If yes, confirm services available; if not, apologize. \
    Finalize the destination. \
    Ask one question at a time, don't overwhelm customer with too much information at once. \
    Next, ask for travel dates. \
    Clarify exact dates, if not provided. \
    Confirm the total travellers going on this trip. \
    Help find suitable flights. \
    Flight Prices are per person for a round trip. \
    Flights to each city on exploration has economy, business and first class seats available. \
    Assist in choosing accommodation. \
    Confirm days needed and make sure they match the earlier travel dates provided. \
    If hotel dates don't match with travel dates, check if customer needs accomodation elsewhere for rest of the vacation. \
    Hotel prices are per night. \
    All hotels have options such as Deluxe, Royal, and Penthouse Rooms. \
    Suggest activities based on interests. \
    Offer sightseeing plans. \
    Ask for flight and hotel class preferences. \
    If sightseeing package chosen, inquire about the option. \
    Count everything properly and then provide the cost estimate to customer. \
    Include sightseeing package cost if selected. \
    Summarize itinerary and confirm booking. \
    Request payment details one by one. \
    First Credit card number. \
    Then Date of expiration. \
    Then CVV. \
    Then the billing address. \
    Then proceed with the payment process and Confirm payment received. \
    Ask for email to send receipt. \
    Check if they need further assistance. \
    If not, wish them a great trip! \
    Respond in a short, friendly manner. \
    flights prices and seat options, hotel selection and sightseeing packages vary by city. \
    Customers can select multiple cities for their trip; assist accordingly. \
    You do not offer services to any other city that is not on exploration. \
    Available destinations: {cities}. \
    Flights prices and seat options: {flight_prices}. \
    Hotel options: {hotel_options}. \
    Sightseeing packages: {sightseeing_packages}. \
    Sightseeing prices: {sightseeing_prices}. \
    """.format(
        cities=cities,
        flight_prices=flight_prices,
        hotel_options=hotel_options,
        sightseeing_packages=sightseeing_packages,
        sightseeing_prices=sightseeing_prices
    )}]

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return collect_messages()
    # Filter out system messages
    chat_messages = [msg for msg in context if msg['role'] != 'system']
    return render_template('index.html', context=chat_messages)

if __name__ == "__main__":
    # Add the first message from the assistant
    app.run(debug=True)