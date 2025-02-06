from flask import Flask, request, jsonify, Response
import json
from flask_cors import CORS
from collections import OrderedDict
import requests

app = Flask(__name__)
CORS(app)

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = str(n)
    num_digits = len(digits)
    total = sum(int(digit) ** num_digits for digit in digits)
    return total == n

# Function to check if a number is perfect
def is_perfect(n):
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Endpoint to classify number
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Error handling for non-integer input
    try:
        number = int(number)
    except ValueError:
        # Manually create an OrderedDict for the error response
        error_response = OrderedDict([
            ("number", number),
            ("error", True)
        ])
        return Response(json.dumps(error_response), mimetype='application/json'), 400

    # Basic properties
    is_prime_number = is_prime(number)
    is_armstrong_number = is_armstrong(number)
    is_perfect_number = is_perfect(number)

    # Determine properties of the number
    properties = []
    if is_armstrong_number:
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Get a fun fact from Numbers API
    fun_fact = get_fun_fact(number)

    # Calculate digit sum
    digit_sum = sum(int(digit) for digit in str(number))

    # Creating OrderedDict to preserve the response order
    response = OrderedDict([
        ("number", number),
        ("is_prime", is_prime_number),
        ("is_perfect", is_perfect_number),
        ("properties", properties),
        ("digit_sum", digit_sum),
        ("fun_fact", fun_fact)
    ])

    # Manually serialize to JSON and return with Response
    return Response(json.dumps(response), mimetype='application/json')

# Function to get a fun fact from the Numbers API
def get_fun_fact(number):
    url = f'http://numbersapi.com/{number}?json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('text', 'No fun fact available.')
    return "No fun fact available."

if __name__ == '__main__':
    app.run(debug=True)
