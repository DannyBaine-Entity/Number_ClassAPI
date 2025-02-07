# Number Classification API

## Overview

The **Number Classification API** is a FastAPI-based web service that classifies numbers based on their mathematical properties. It determines whether a number is prime, Armstrong, or perfect, and also provides additional insights like its parity (even/odd), digit sum, and a fun fact from the Numbers API.

## Features

- Classifies numbers as prime, Armstrong, or perfect.
- Determines if a number is even or odd.
- Computes the sum of digits.
- Fetches fun facts about the number from an external API.
- Returns structured JSON responses.

## API Endpoints

### 1. Classify Number

**Endpoint:**

`GET /api/classify-number`

**Query Parameters:**

| Parameter | Type   | Required | Description               |
|-----------|--------|----------|---------------------------|
| number    | string | Yes      | The number to be classified. |

**Response Structure:**

**Success Response (200 OK)**

```json
{
  "number": 153,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "digit_sum": 9,
  "fun_fact": "153 is a narcissistic number."
}
```

**Error Responses**

Invalid input (not a number):

```json
{
    "number": "alphabet",
    "error": true,
    "message": "Invalid input. Please provide a valid number."
}
```
Negative number:

```json
{
    "number": "Negative",
    "error": true,
    "message": "Negative numbers are not allowed."
}
```

## Installation & Setup

### Clone the repository

```bash
git clone https://github.com/your-repo/number-classification-api.git
cd number-classification-api
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
uvicorn main:app --reload
```

## Technologies Used

- FastAPI
- Requests
- Pydantic
- Uvicorn
- Numbers API
- Python 3
