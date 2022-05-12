import sqlite3

connection = sqlite3.connect("Data.db")

cursor = connection.cursor()

create_table_query="CREATE TABLE User(id int,username text, password text)"

cursor.execute(create_table_query)

insertQuery="INSERT INTO User values(?,?,?)"

users=[(1,'kishan','santlani'),(2,'chegg','expert')]

cursor.executemany(insertQuery,users)

connection.commit()

selectQuery="SELECT * FROM User"

result=cursor.execute(selectQuery)

for row in result:
    print(row)