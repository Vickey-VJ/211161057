from flask import Flask, jsonify
import math
import random
import time
from collections import deque

app = Flask(__name__)

# Constants
WINDOW_SIZE = 10
number_window = deque()

# Helper function to calculate average
def calculate_average(numbers):
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

# Function to generate Fibonacci sequence up to n
def fibonacci(n):
    fib_list = [0, 1]
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
        fib_list.append(b)
    return fib_list

# Function to check if a number is even
def is_even(num):
    return num % 2 == 0

# Function to check if a number is odd
def is_odd(num):
    return num % 2 != 0

# Endpoint
@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    global number_window

    start_time = time.time()
    p = 0
    q = 10000
    previous_state = list(number_window)

    # Determine the actual numberid based on input
    if numberid == 'e':
        numberid = 'even'
        evens = [i for i in range(p, q) if is_even(i)]
        n = random.sample(evens, min(10, len(evens)))
        number_window.extend(n)
    elif numberid == 'o':
        numberid = 'odd'
        odds = [i for i in range(p, q) if is_odd(i)]
        n = random.sample(odds, min(10, len(odds)))
        number_window.extend(n)
    elif numberid == 'p':
        numberid = 'prime'
        primes = [i for i in range(p, q) if is_prime(i)]
        n = random.sample(primes, min(10, len(primes)))
        number_window.extend(n)
    elif numberid == 'f':
        numberid = 'fibonaaci'
        fibo = fibonacci(100)
        n = random.sample(fibo, 10)
        number_window.extend(n)
    elif numberid == 'r':
        numberid = 'random'
        randoms = random.sample(range(p, q), 10)
        number_window.extend(randoms)
    else:
        return jsonify({'error': 'Invalid numberid'}), 400

    # Keep only the last WINDOW_SIZE numbers in the deque
    if len(number_window) > WINDOW_SIZE:
        number_window = deque(list(number_window)[-WINDOW_SIZE:])

    # Calculate average of current window
    avg = calculate_average(number_window)

    # Prepare response
    response_obj = {
        'numbers': list(number_window),
        'windowPrevState': previous_state,
        'windowCurrState': list(number_window),
        'avg': f"{avg:.2f}"
    }

    # Calculate time taken for fetching numbers
    time_taken = time.time() - start_time
    print(f"Time taken: {time_taken:.2f} seconds")

    return jsonify(response_obj), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=9876)