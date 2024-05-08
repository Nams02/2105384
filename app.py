from flask import Flask, request, jsonify
import requests

WINDOW_SIZE = 10

app = Flask(__name__)


@app.route('/numbers/<string:numberid>')
def calculate_average(numberid):
    valid_numberids = ['p', 'f', 'e', 'r']
    if numberid not in valid_numberids:
        return jsonify({'error': 'Invalid numberid'}), 400

    if numberid == 'p':
        url = 'http://20.244.56.144/test/primes'
    elif numberid == 'f':
        url = 'http://20.244.56.144/test/fibo'
    elif numberid == 'e':
        url = 'http://20.244.56.144/test/even'
    elif numberid == 'r':
        url = 'http://20.244.56.144/test/rand'

    numbers = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        fetched_numbers = response.json().get('numbers', [])
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch numbers from Test Server API'}), 500

    if len(numbers) + len(fetched_numbers) <= WINDOW_SIZE:
        numbers.extend(fetched_numbers)
        average = sum(numbers) / len(numbers) if numbers else 0
    else:
        numbers = fetched_numbers[-WINDOW_SIZE:]
        average = sum(numbers) / WINDOW_SIZE

    response_data = {
        'windowCurrState': numbers[-WINDOW_SIZE:],
        'numbers': fetched_numbers,
        'avg': average
    }

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)
