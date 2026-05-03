import happybase

connection = happybase.Connection('localhost', port=9090)

table_name = 'transport'

families = {
    'bus': dict(),
    'trip': dict(),
    'geo': dict(),
    'meta': dict()
}

if table_name.encode() not in connection.tables():
    connection.create_table(table_name, families)
    print("Table created")
else:
    print("Table already exists")