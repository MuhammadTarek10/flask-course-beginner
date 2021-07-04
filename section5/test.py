import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

omar_user = (1, "Omar", "omar_password")
insert_user_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_user_query, omar_user)


many_users = [
                (2, "amira", "amira_password"),
                (3, "khaled", "khaled_password")
             ]

cursor.executemany(insert_user_query, many_users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)


connection.commit()
connection.close()
