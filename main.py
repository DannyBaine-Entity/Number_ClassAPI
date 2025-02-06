from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import requests
from collections import OrderedDict

# Create FastAPI instance
app = FastAPI()

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    if n < 0:  # Reject negative numbers
        return False
    digits = str(abs(n))  # Use absolute value to avoid negative sign
    num_digits = len(digits)
    total = sum(int(digit) ** num_digits for digit in digits)
    return total == abs(n)

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    if n < 0:  # Reject negative numbers
        return False
    divisors = [i for i in range(1, abs(n)) if n % i == 0]  # Use absolute value
    return sum(divisors) == abs(n)

# Function to get a fun fact from the Numbers API
def get_fun_fact(number: int) -> str:
    url = f'http://numbersapi.com/{number}?json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('text', 'No fun fact available.')
    return "No fun fact available."

# Endpoint to classify number
@app.get("/api/classify-number")
async def classify_number(number: Optional[str] = None):
    # Initial classification
    classification = "unknown"

    # Check if the input is negative
    if number is not None and number.startswith("-"):
        classification = "negative"

    # Try converting the string input to an integer
    try:
        if number is not None:
            # If the string is a valid number (including negative numbers), classify as integer
            number_int = int(number)
            classification = "integer"
        else:
            # If no number provided, classify as alphabet
            classification = "alphabet"
    except ValueError:
        # If conversion fails, classify as alphabet
        classification = "alphabet"

    # If input is classified as alphabet or negative, return a classification error
    if classification in ["alphabet", "negative"]:
        error_response = OrderedDict([
            ("classification", classification),
            ("error", True)
        ])
        return JSONResponse(status_code=400, content=error_response)

    # Basic properties if it's an integer
    number_int = int(number)
    is_prime_number = is_prime(number_int)
    is_armstrong_number = is_armstrong(number_int)
    is_perfect_number = is_perfect(number_int)

    # Determine properties of the number
    properties = []
    if is_armstrong_number:
        properties.append("armstrong")
    if number_int % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Get a fun fact from Numbers API
    fun_fact = get_fun_fact(number_int)

    # Calculate digit sum using the absolute value of the number
    digit_sum = sum(int(digit) for digit in str(abs(number_int)))  # Use absolute value for digit sum

    # Creating OrderedDict to preserve the response order
    response = OrderedDict([
        ("number", number_int),
        ("is_prime", is_prime_number),
        ("is_perfect", is_perfect_number),
        ("properties", properties),
        ("digit_sum", digit_sum),
        ("fun_fact", fun_fact)
    ])

    # Return response as JSON
    return JSONResponse(content=response)

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)