from flask import Flask,jsonify
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

def list_dicts_factory(cursor, row):
    list = {}
    number = 0   
    d = {}
    for index, col in enumerate(cursor.description):
        
        if col[0] in d:
            list[number] = d
            number += 1
            d = {}

        d[col[0]] = row[index]

    list[number] = d

    return list

def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]

    return d

@app.route('/r/posts/<int:post_id>/comments', methods = ['GET'])
def retrive_post_CONTENT(post_id):
    # pass
    conn = sqlite3.connect('otaku.db')
    conn.row_factory = list_dicts_factory
    cur = conn.cursor()
    all_posts = cur.execute('SELECT * FROM Posts  INNER JOIN comments \
        ON Posts.post_id = comments.post_id WHERE Posts.post_id = {};'.format(post_id)).fetchall()

    return jsonify(all_posts)
    

@app.route('/r/all', methods=['GET'])
def home():
    #shows post
    conn = sqlite3.connect('otaku.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_posts = cur.execute('SELECT * FROM Posts;').fetchall()



    return jsonify(all_posts)
    # return '''<h1>A weeb's sad tale</h1>
    # <p>Vader: Your feelings for your waifu are not real<br>
    # StarKiller: THEY ARE TO ME!</p>'''



@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404 NOT FOUND (i think)</h1><p>{}</p>'''.format(e), 404


app.run()