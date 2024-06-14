import json
from datetime import datetime
from flask import Flask, request, jsonify
from sql_connection import get_sql_connection
import product_dao
import uom_dao
import order_dao  # Assuming the module where insert_order is defined

# Establish a connection to the database
connection = get_sql_connection()

app = Flask(__name__)


@app.route('/getProducts')
def get_products():
    product = product_dao.get_all_product(connection)
    response = jsonify(product)
    response.headers.add('Access-Control-Allow-Origin', '*')  # Corrected method name
    return response


@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uom(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = product_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_new_product():
    request_payload = json.loads(request.form['data'])
    product_id = product_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order_route():
    try:
        request_payload = json.loads(request.data)

        # Assuming request_payload contains 'customer_name', 'grand_total', 'order_details'
        order_data = {
            'customer_name': request_payload['customer_name'],
            'grand_total': request_payload['grand_total'],
            'datetime': datetime.now(),
            'order_details': request_payload['order_details']
        }

        order_id = order_dao.insert_order(connection, order_data)  # Correctly referencing insert_order function

        response = jsonify({
            'order_id': order_id,
            'message': 'Order inserted successfully'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        error_message = f"Failed to insert order: {str(e)}"
        print(error_message)
        response = jsonify({
            'error': error_message
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


if __name__ == "__main__":
    print("Starting python flask server for Grocery store Management System")
    app.run(port=5000)
