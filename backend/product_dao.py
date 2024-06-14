from sql_connection import get_sql_connection


def get_all_product(connection):
    cursor = connection.cursor()
    query = ("SELECT product.product_id, product.name, product.uom_id, product.price_per_unit, uom.uom_name "
             "FROM product "
             "INNER JOIN uom ON product.uom_id = uom.uom_id")

    cursor.execute(query)

    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append(
            {
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            }
        )

    cursor.close()  # Close cursor after use
    return response


# To add new product to the database
def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO product "
             "(name, uom_id, price_per_unit) "
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])
    cursor.execute(query, data)
    connection.commit()

    last_row_id = cursor.lastrowid  # Capture the last inserted ID before closing the cursor
    cursor.close()  # Close cursor after use
    return last_row_id


# To delete product from the database
def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = "DELETE FROM product WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    connection.commit()

    affected_rows = cursor.rowcount  # Capture the number of rows affected
    cursor.close()  # Close cursor after use
    return affected_rows


if __name__ == '__main__':
    connection = get_sql_connection()

    # Insert a new product and print the new product ID
    new_product_id = insert_new_product(connection, {
        'product_name': 'bean',
        'uom_id': 1,
        'price_per_unit': 500.0
    })
    print(f'New product ID: {new_product_id}')

    # Delete a product and print the number of affected rows
    rows_deleted = delete_product(connection, 26)
    print(f'Number of products deleted: {rows_deleted}')

    connection.close()  # Close the connection after operations are complete
