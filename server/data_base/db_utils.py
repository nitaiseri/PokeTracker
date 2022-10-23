
# def parse_return_values_from_db()

def create_insert_query(table_name, rows):
    query = f'INSERT INTO {table_name} VALUES'
    for row in rows:
        row_string = str(row)[1:-1]
        query += f'({row_string}),'
    return query[:-1] + ";"