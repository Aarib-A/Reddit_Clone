from flask import Flask,jsonify, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

def Connect_to_db(need_dicts_factory = False):
    conn = sqlite3.connect('otaku.db')
    if need_dicts_factory is True:
        conn.row_factory = dict_factory
    else:
        conn.row_factory = list_dicts_factory
    cur = conn.cursor()
    return conn, cur

def Close_db(conn, cur):
    try:
        cur.close()
        conn.close()
    except:
        return False
    
    return True

@app.route('/LogIN', methods=['POST', 'GET'])
def login(): # The code is similar to https://flask.palletsprojects.com/en/1.1.x/quickstart/
    #  if request.method == 'POST':
    #      if valid_login(request.form['UserName'],
    #                     request.form['Psswrd']):
    #         return lo
    pass

#CHANGE TO ONLY GIVE A DICT (UPDATE: THIS IS NOT NEEDED ANYMORE)
def list_dicts_factory(cursor, row):
    # list = []
    list = {}
    # list = dictionary_obj
    # number = 0   
    # number = start_from
    d = {}
    for index, col in enumerate(cursor.description):
        
        # if col[0] in d:
            # list[number] = d
            # list.append(d)
            # number += 1
            # d = {}

        d[col[0]] = row[index]

    # list[number] = d
    # list.append(d)
    # list['result'] = d

    return list


#USE this only
def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]

    return d


#CHANGE THE QUERY
def insert_into_posts(conn, task): #https://www.sqlitetutorial.net/sqlite-python/insert/
    #must change the parameter feilds, they notw
    #NOW THEY ARE CHANGED
    sql = ''' INSERT INTO Posts(Owner_ID, owner_name,post_id, post_title, post_body, upvotes, downvotes, date, comm_name, karma)
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

    cur.close()
    connection.close()
    return redirect(url_for('home'))

#CHANGE TUPLE FIELD
@app.route('/r/<community>/submit', methods = ['GET', 'POST'])
def preparing_reddite_post(community):
    if request.method == 'GET':
        return render_template('submit.html')
    elif request.method == 'POST':
        conn, cur = Connect_to_db()
        data = request.get_json()
        date_stamp = str(datetime.utcnow())
        # post_title = request.form['post-title']
        # post_body = request.form['post-body']
        post_title = data['post_title']
        post_body = data['post_body']
        post_id = data['post_id']
        owner_id = data['owner_id']
        owner_name = data['owner_name']
        #INCLUDE DATABASE VARIABLES IN THIS TUPLE (UPDATE, DID IT)
        # tupl = (9000, 'Filthy Frank',1200, post_title, post_body, 1, 0, date_stamp, community, 1)
        tupl = (owner_id, owner_name, post_id, post_title, post_body, 1,0, date_stamp , community, 1)

        with conn:
            row_id = insert_into_posts(conn, tupl)

        Close_db(conn=conn, cur=cur)
    return redirect(url_for('retrive_post_CONTENT', post_id = 1200))

def vote(community, post_id, is_increment):
    conn, cur = Connect_to_db()
    if is_increment:
        cur.execute("UPDATE Posts \
                 SET upvotes = upvotes + 1 , karma = karma + 1\
                 WHERE comm_name = '{}' AND post_id = {};".format(community,post_id))

    else:
        cur.execute("UPDATE Posts \
                SET downvotes = downvotes + 1 , karma = karma - 1\
                WHERE comm_name = '{}' AND post_id = {};".format(community,post_id))

    conn.commit()
    Close_db(conn, cur)

@app.route('/r/<community>/posts/<int:post_id>/karma/increment', methods = ['PUT']) #must find way to send status code '200'
def increment_post(community, post_id): 
    vote(community=community, post_id=post_id, is_increment=True)
    return redirect(url_for('retrive_post_CONTENT', community = community, post_id = post_id))
    
@app.route('/r/<community>/posts/<int:post_id>/karma/decrement', methods = ['PUT']) #must find way to send status code '200'
def decrement_post(community, post_id): 
    vote(community=community, post_id=post_id, is_increment=False)
    return redirect(url_for('retrive_post_CONTENT', community = community, post_id = post_id))

@app.route('/r/<community>/posts/<int:post_id>/comments', methods = ['GET'])
def retrive_post_CONTENT(community, post_id):
    conn,cur = Connect_to_db(need_dicts_factory=True)
    post_content = cur.execute("SELECT * FROM Posts  \
         WHERE Posts.post_id = {} AND Posts.comm_name = '{}';".format(post_id, community)).fetchall()
    comments = cur.execute('SELECT * FROM comments  \
         WHERE comments.post_id = {} ORDER BY date DESC;'.format(post_id)).fetchall()
    Close_db(conn=conn, cur=cur)

    whole_dict ={}
    whole_dict["post"] = post_content[0]
    whole_dict['comments'] = comments
    return jsonify(whole_dict)

    


@app.route('/r/<community>', methods = ["GET"])
def commmunity_posts(community):
    conn, cur = Connect_to_db(need_dicts_factory=True)
    all_community_posts = cur.execute("SELECT * FROM Posts \
                                       WHERE Posts.comm_name = '{}' \
                                       ORDER BY date DESC \
                                       LIMIT 20;".format(community)).fetchall()    
    Close_db(conn, cur)
    return jsonify(all_community_posts)
    
    
@app.route('/r/all', methods=['GET'])
def topPosts():
    conn, cur = Connect_to_db(need_dicts_factory=True)
    all_posts = cur.execute('SELECT * FROM Posts \
                             ORDER BY karma DESC \
                             LIMIT 20;').fetchall()

    Close_db(conn, cur)
    results = {}
    results['posts'] = all_posts
    return jsonify(results)

@app.route('/', methods=['GET'])
def home():
    #shows post
    conn, cur = Connect_to_db()
    all_posts = cur.execute('SELECT * FROM Posts \
                             ORDER BY date DESC \
                             LIMIT 20;').fetchall()
    Close_db(conn, cur)


    return jsonify(all_posts)
    # return '''<h1>A weeb's sad tale</h1>
    # <p>Vader: Your feelings for your waifu are not real<br>
    # StarKiller: THEY ARE TO ME!</p>'''

@app.route('/sort', methods = ['GET'])
def sort_post_id():
    
    list = request.args['list']
    list = list.split(',')
    print(list[0])
    for i in range(0, len(list)):
        list[i] = int(list[i])
    list = top_posts_from_list(list)
    return list


def top_posts_from_list(someList):
    conn, cur = Connect_to_db(need_dicts_factory=True)
    top_scoring_posts = cur.execute("SELECT * FROM Posts \
                                     WHERE post_id IN {} \
                                     ORDER BY karma DESC;".format(tuple(someList))).fetchall()
    Close_db(conn, cur)
    return jsonify(top_scoring_posts)



@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404 NOT FOUND (i think)</h1><p>{}</p>'''.format(e), 404


app.run()

# print(top_posts_from_list([1200, 787]))

