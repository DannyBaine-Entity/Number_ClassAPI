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
    digits = str(n)
    num_digits = len(digits)
    total = sum(int(digit) ** num_digits for digit in digits)
    return total == n

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Function to get a fun fact from the Numbers API
def get_fun_fact(number: int) -> str:
    url = f'http://numbersapi.com/{number}?json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('text', 'No fun fact available.')
    return "No fun fact available."

# Function to create error response
def create_error_response(input_value: str, classification: str, message: str):
    return JSONResponse(
        status_code=400,
        content=OrderedDict([
            ("input", input_value),
            ("classification", classification),
            ("error", True),
            ("message", message)
        ])
    )

# Endpoint to classify number
@app.get("/api/classify-number")
async def classify_number(number: Optional[str] = None):
    if not number or not number.lstrip('-').isdigit():
        return create_error_response(number, "alphabet", "Invalid input: not a number.")

    if number.startswith("-"):
        return create_error_response(number, "negative", "Negative numbers are not allowed.")

    number_int = int(number)
    is_prime_number = is_prime(number_int)
    is_armstrong_number = is_armstrong(number_int)
    is_perfect_number = is_perfect(number_int)

    properties = ["even" if number_int % 2 == 0 else "odd"]
    if is_armstrong_number:
        properties.append("armstrong")

    fun_fact = get_fun_fact(number_int)
    digit_sum = sum(int(digit) for digit in str(number_int))

    response = OrderedDict([
        ("number", number_int),
        ("is_prime", is_prime_number),
        ("is_perfect", is_perfect_number),
        ("properties", properties),
        ("digit_sum", digit_sum),
        ("fun_fact", fun_fact)
    ])

    return JSONResponse(content=response)

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)