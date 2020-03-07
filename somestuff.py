import sqlite3
from flask import jsonify, Flask

app = Flask(__name__)

# conn = sqlite3.connect("otaku.db")

# cursor = conn.cursor()


# for i in cursor.execute("SELECT * FROM Posts;"):
#     print(i)
#     list.append(i)

# print(str(list))


@app.route('/')
def default():
    return "Hello Doe"

@app.route('/u/<userid>')
def user():
    pass

@app.route('/r/<community>')
def community():
    pass

@app.route('/r/<community>/<post>/')
def post():
    pass

@app.route('/r/<community>/<post>/>comment>/')
def comment():
    pass


if __name__ == '__main__':
    app.run()


