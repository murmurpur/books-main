from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

INVENTORY_SERVICE_URL = 'http://localhost:5000'

@app.route('/orders', methods=['GET'])
def get_orders():
    # Placeholder for getting orders
    return jsonify({'message': 'List of orders'})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    book_id = data['book_id']
    
    # Call Inventory Service to update stock
    book_response = requests.get(f'{INVENTORY_SERVICE_URL}/books/{book_id}')
    
    # Log the response from the Inventory Service
    app.logger.info('Inventory service response: Status Code %s, Response Text %s', book_response.status_code, book_response.text)
    
    # Check if the request to the Inventory Service was successful
    if book_response.status_code != 200:
        return jsonify({'message': 'Error communicating with Inventory Service', 'status_code': book_response.status_code}), book_response.status_code
    
    # Handle JSON decoding in a try-except block
    try:
        book_data = book_response.json()
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        app.logger.error('Decoding JSON has failed')
        return jsonify({'message': 'Decoding JSON has failed'}), 500
    
    # Check if the book is in stock
    if book_data.get('stock_quantity', 0) <= 0:
        return jsonify({'message': 'Book out of stock'}), 400

    # Here we would ideally have logic to create an order and reduce stock, but this is a placeholder
    return jsonify({'message': 'Order created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=6000)
