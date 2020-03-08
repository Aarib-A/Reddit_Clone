from flask import Flask,jsonify, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/LogIN', methods=['POST', 'GET'])
def login(): # The code is similar to https://flask.palletsprojects.com/en/1.1.x/quickstart/
    #  if request.method == 'POST':
    #      if valid_login(request.form['UserName'],
    #                     request.form['Psswrd']):
    #         return lo
    pass

def list_dicts_factory(cursor, row):
    list = []
    # list = {}
    # list = dictionary_obj
    # number = 0   
    # number = start_from
    d = {}
    for index, col in enumerate(cursor.description):
        
        if col[0] in d:
            # list[number] = d
            list.append(d)
            # number += 1
            # d = {}

        d[col[0]] = row[index]

    # list[number] = d
    list.append(d)

    return list

def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]

    return d



def insert_into_posts(conn, task): #https://www.sqlitetutorial.net/sqlite-python/insert/
    sql = ''' INSERT INTO Posts(Owner_ID, owner_name,post_id, post_title, post_body, upvotes, downvotes, date)
                    VALUES(?,?,?,?,?,?,?,?) ;'''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid

@app.route('/r/post/<int:post_id>/del', methods = ["POST"])
def killiing_post(post_id):
    connection = sqlite3.connect("otaku.db")
    cur = connection.cursor()
    cur.execute("DELETE FROM Posts WHERE Posts.post_id={};".format(post_id))
    connection.commit()
    cur.execute("DELETE FROM comments WHERE comments.post_id={};".format(post_id))
    connection.commit()
    # connection.execute("DELETE FROM Posts WHERE Posts.post_id={};".format(post_id))
    # connection.execute("DELETE FROM comments WHERE comments.post_id={};".format(post_id))
    cur.close()
    connection.close()
    return redirect(url_for('home'))

@app.route('/submit', methods = ['GET', 'POST'])
def preparing_reddite_post():
    if request.method == 'GET':
        return render_template('submit.html')
    elif request.method == 'POST':
        conn = sqlite3.connect('otaku.db')
        date_stamp = str(datetime.utcnow())
        post_title = request.form['post-title']
        post_body = request.form['post-body']
        tupl = (9000, 'Filthy Frank',1200, post_title, post_body, 1, 0, date_stamp)

        with conn:
            row_id = insert_into_posts(conn, tupl)
   
        conn.close()
        # return jsonify(all_posts)
    return redirect(url_for('retrive_post_CONTENT', post_id = 1200))


@app.route('/r/posts/<int:post_id>/comments', methods = ['GET'])
def retrive_post_CONTENT(post_id):
    # pass
    conn = sqlite3.connect('otaku.db')
    conn.row_factory = list_dicts_factory
    cur = conn.cursor()
    # all_posts = cur.execute('SELECT * FROM Posts LEFT JOIN comments \
    #     ON Posts.post_id = comments.post_id  WHERE Posts.post_id = {};'.format(post_id)).fetchall()
    post_content = cur.execute('SELECT * FROM Posts  \
         WHERE Posts.post_id = {};'.format(post_id)).fetchall()
    
    comments = cur.execute('SELECT * FROM comments  \
         WHERE comments.post_id = {} ORDER BY date DESC;'.format(post_id)).fetchall()
    # conn.commit()
    conn.close()

    whole_dict ={}
    # whole_dict["post"] = post_content[0]
    # whole_dict["comments"] = comments
    whole_dict["post"] = post_content[0]
    whole_dict['comments'] = {}
    for i in range(len(comments)):
        whole_dict['comments'][i] = comments[i]

    return jsonify(whole_dict)
    # return jsonify(all_posts)
    

@app.route('/r/all', methods=['GET'])
def home():
    #shows post
    conn = sqlite3.connect('otaku.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_posts = cur.execute('SELECT * FROM Posts;').fetchall()
    conn.commit()
    conn.close()


    return jsonify(all_posts)
    # return '''<h1>A weeb's sad tale</h1>
    # <p>Vader: Your feelings for your waifu are not real<br>
    # StarKiller: THEY ARE TO ME!</p>'''



@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404 NOT FOUND (i think)</h1><p>{}</p>'''.format(e), 404


app.run()