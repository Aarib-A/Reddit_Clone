import sqlite3
from flask import jsonify

conn = sqlite3.connect("otaku.db")

cursor = conn.cursor()


for i in cursor.execute("SELECT * FROM Posts;"):
    print(i)
    list.append(i)

print(str(list))


