from datetime import datetime
from sql_connection import get_sql_connection


def insert_order(connection, order):
    try:
        cursor = connection.cursor()

        # Insert into `order` table
        order_query = ("INSERT INTO `order` "
                       "(customer_name, total, datetime) "
                       "VALUES (%s, %s, %s)")
        order_data = (order['customer_name'], float(order['grand_total']), datetime.now())

        cursor.execute(order_query, order_data)
        order_id = cursor.lastrowid

        # Insert into `order_details` table
        order_details_query = ("INSERT INTO order_details "
                               "(order_id, product_id, quantity, total_price) "
                               "VALUES (%s, %s, %s, %s)")

        order_details_data = []
        for order_detail in order['order_details']:
            order_details_data.append((
                order_id,
                int(order_detail['product_id']),
                int(order_detail['quantity']),
                float(order_detail['total_price'])
            ))

        cursor.executemany(order_details_query, order_details_data)
        connection.commit()

        return order_id

    except Exception as e:
        print(f"Error inserting order: {e}")
        connection.rollback()
        return None

    finally:
        cursor.close()


if __name__ == '__main__':
    connection = get_sql_connection()

    order_data = {
        'customer_name': 'Hulk',
        'grand_total': '500',  # Assuming grand_total should be a numeric value
        'datetime': datetime.now(),
        'order_details': [
            {
                'product_id': 10,
                'quantity': 2,
                'total_price': 50,
            },
            {
                'product_id': 23,
                'quantity': 3,
                'total_price': 30,
            }
        ]
    }

    print(insert_order(connection, order_data))
    connection.close()
