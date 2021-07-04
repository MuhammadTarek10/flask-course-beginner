import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


create_users_tabel_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users_tabel_query)

create_items_table_query = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_items_table_query)


connection.commit()
connection.close()
