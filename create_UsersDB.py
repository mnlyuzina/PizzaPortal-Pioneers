import sqlite3

connection = sqlite3.connect('users_database.db')
cursor = connection.cursor()
columns = ["id INTEGER PRIMARY KEY", "lname VARCHAR", "fname VARCHAR", "phone_number INTEGER UNIQUE", "address VARCHAR"]

query_create_table = f"CREATE TABLE IF NOT EXISTS users ({', '.join(columns)})"
connection.execute(query_create_table)

data = ["1, 'Dubrovina', 'Sofya', 89776833233, ''"]

for user in data:
    query_insert_data = f"INSERT INTO users VALUES ({user})"
    cursor.execute(query_insert_data)

connection.commit()