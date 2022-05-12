import sqlite3

connection = sqlite3.connect("Data.db")

cursor = connection.cursor()

create_table_user_query="CREATE TABLE IF NOT EXISTS User(id INTEGER Primary Key,username text, password text)"
print("Table created successfully")
cursor.execute(create_table_user_query)

create_table_item_query="CREATE TABLE IF NOT EXISTS Item(id INTEGER Primary Key,name text, price real)"
cursor.execute(create_table_item_query)

connection.commit()
connection.close()
