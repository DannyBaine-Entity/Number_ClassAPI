from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import requests
from collections import OrderedDict

# Create FastAPI instance
# Create FastAPI instance
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# Endpoint to classify number
@app.get("/api/classify-number")
async def classify_number(number: int):
    # Error handling for non-integer input
    if not isinstance(number, int):
        error_response = OrderedDict([
            ("number", number),
            ("error", True)
        ])
        return JSONResponse(status_code=400, content=error_response)

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

    # Return response as JSON
    return JSONResponse(content=response)

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
