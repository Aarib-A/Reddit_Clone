from database import *
from flask import Flask, jsonify, request, redirect, url_for, abort, Response
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

def create_new_post(conn, cur, task):
    sql = '''INSERT INTO Posts(id, user_id, community, date, post_title, post_body)
                    VALUES(?, ?, ?, ?, ?, ?); '''
    
    cur.execute(sql, task)
    conn.commit()

    # Create Votes row
    create_new_vote(task[0])

    return cur.lastrowid

def create_new_vote(post_id):
    conn, cur = Connect_to_db('Votes')
    sql = '''INSERT INTO Votes(post_id, upvotes, downvotes, karma) 
                    VALUES(?, ?, ?, ?); '''
    values = (post_id, 1, 0, 1)
    cur.execute(sql, values)
    conn.commit()
    Close_db(conn, cur)

# SUBMIT A POST
def submit(data):
    conn, cur = Connect_to_db('Posts')

    post_id = data['post_id']
    user_id = data['user_id']
    community = data['community']
    date = str(datetime.utcnow())
    post_title = data['post_title']
    post_body = data['post_body']

    task = (post_id, user_id, community, date, post_title, post_body)
    try: 
        with conn:
            create_new_post(conn=conn, cur=cur, task=task)

    except sqlite3.IntegrityError as e:
        Close_db(conn=conn, cur=cur)
        abort(409)

    Close_db(conn=conn, cur=cur)
    status_code = Response(status=201)
    return status_code

# RETRIEVE COMMUNITY POSTS
def retrieve_community_posts(community):
    conn, cur = Connect_to_db(option='Posts', need_dicts_factory=True)
    all_community_posts = cur.execute("SELECT * FROM Posts \
                                                WHERE Posts.community = '{}' \
                                                ORDER BY date DESC \
                                                LIMIT 20".format(community)).fetchall()

    Close_db(conn, cur)
    results = {}
    results['results'] = all_community_posts
    return jsonify(results)

# RETRIEVE ALL POSTS
def retrieve_all_posts():
    conn, cur = Connect_to_db(option='Posts', need_dicts_factory=True)
    
    all_posts = cur.execute('SELECT * FROM Posts \
                             ORDER BY date DESC \
                             LIMIT 20').fetchall()
    Close_db(conn, cur)

    results = {}
    results['posts'] = all_posts
    return jsonify(results)

# RETRIEVE A SINGLE POST 
def retrieve_post_content(post_id):
    conn, cur = Connect_to_db(option='Posts', need_dicts_factory=True)

    post_content = cur.execute("SELECT * FROM Posts\
                                WHERE Posts.id = {};".format(post_id)).fetchall()
    Close_db(conn=conn, cur=cur)

    return jsonify(post_content[0])

# DELETING A POST 
def delete_post(post_id):
    post_conn, post_cur = Connect_to_db('Posts')
    vote_conn, vote_cur = Connect_to_db('Votes')

    post_cur.execute("DELETE FROM Posts WHERE Posts.id={}".format(post_id))
    post_conn.commit()

    # DELETE FROM VOTES TABLE AS WELL 
    vote_cur.execute("DELETE FROM Votes WHERE post_id={}".format(post_id))
    vote_conn.commit()

    Close_db(conn=post_conn, cur=post_cur)
    Close_db(conn=vote_conn, cur=vote_cur)

    status_code = Response(status=200)
    return status_code 

@app.route('/Post', methods = ["GET", "POST"])
def Post():
    data = request.get_json()
    command = data['command']
    # Process GET requests
    if request.method == 'GET':
        # GET A COMMUNITY'S POSTS
        if command == 'community':
            return retrieve_community_posts(data['community'])

        # GET ALL POSTS
        elif command == 'all':
            return retrieve_all_posts()

        # GET A CERTAIN POST 
        elif command == 'retrieve':
            return retrieve_post_content(data['post_id'])

    # Process POST requests
    elif request.method == 'POST':

        # SUBMIT A POST
        if command == 'submit':
            return submit(data)

        #DELEE A POST
        elif command == 'delete':
            return delete_post(data['post_id'])

@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404 NOT FOUND</h1><p>{}</p>'''.format(e), 404

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)



