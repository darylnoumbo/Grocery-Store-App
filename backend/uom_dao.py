def get_uom(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM uom"  # Corrected 'form' to 'FROM'
    cursor.execute(query)

    response = []
    for (uom_id, uom_name) in cursor:
        response.append({
            'uom_id': uom_id,
            'uom_name': uom_name
        })

    cursor.close()  # Close the cursor after use
    return response

if __name__ == '__main__':
    from sql_connection import get_sql_connection

    connection = get_sql_connection()
    uom_data = get_uom(connection)
    print(uom_data)
