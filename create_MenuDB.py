import sqlite3

connection = sqlite3.connect('menu_database.db')
cursor = connection.cursor()

query_create_table = f"CREATE TABLE IF NOT EXISTS pizzas (pizza VARCHAR UNIQUE, price VARCHAR, diameter VARCHAR)"
connection.execute(query_create_table)

query_create_table = f"CREATE TABLE IF NOT EXISTS beverages (beverage VARCHAR UNIQUE, price VARCHAR, volume VARCHAR)"
connection.execute(query_create_table)

pizzas_menu = ["'Cheesy', '539 RUB', '30 sm'", "'Pepperoni', '729 RUB', '30 sm'", "'Double Chicken', '619 RUB', '30 sm'", "'Chorizo', '539 RUB', '30 sm'", "'Julienne', '799 RUB', '30 sm'", "'Pesto', '799 RUB', '30 sm'", "'Carbonara', '899 RUB', '30 sm'", "'Meat Feast', '799 RUB', '30 sm'", "'Hawaiian', '729 RUB', '30 sm'", "'BBQ Chicken', '899 RUB', '30 sm'", "'Margherita', '729 RUB', '30 sm'", "'Diablo', '899 RUB', '30 sm'", "'Vegeterian', '799 RUB', '30 sm'"]

for data in pizzas_menu:
    query_insert_data = f"INSERT INTO pizzas VALUES ({data})"
    cursor.execute(query_insert_data)

beverages_menu = ["'Water', '70 RUB', '0.5 l'", "'Coca-Cola', '135 RUB', '0.5 l'", "'Sprite', '135 RUB', '0.5 l'", "'Dr Peper', '135 RUB', '0.5 l'", "'Fanta', '135 RUB', '0.5 l'", "'Lemonade', '135 RUB', '0.5 l'", "'Sweet Tea', '139 RUB', '0.5 l'", "'Hot Tea', '139 RUB', '0.5 l'", "'Orange Juice', '125 RUB', '0.5 l'", "'Apple Juice', '125 RUB', '0.5 l'", "'Cherry Juice', '125 RUB', '0.5 l'", "'Cocoa', '129 RUB', '0.3 l'", "'Hot Chocolate', '159 RUB', '0.4 l'"]

for data in beverages_menu:
    query_insert_data = f"INSERT INTO beverages VALUES ({data})"
    cursor.execute(query_insert_data)

connection.commit()