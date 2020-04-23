from database import *
from flask import Flask, jsonify, request, Response, abort 

app = Flask(__name__)
app.config["DEBUG"] = True

def voting(post_id, is_upvote):
    conn, cur = Connect_to_db('Votes')
    change, symbol = None, None
    # Upvoting 
    if is_upvote:
        change, symbol = 'upvotes', '+'
    # Downvoting
    else:
        change, symbol = 'downvotes', '-'
    
    cur.execute("UPDATE Votes \
             SET {} = {} + 1, karma = karma {} 1 \
             WHERE post_id = {}".format(change, change, symbol, post_id))

    conn.commit()
    Close_db(conn=conn, cur=cur)
    
    status_code = Response(status=200)
    return status_code

def report(post_id):
    conn, cur = Connect_to_db('Votes', need_dicts_factory=True)

    result = cur.execute("SELECT * FROM Votes \
                          WHERE post_id = {}".format(post_id)).fetchall()

    Close_db(conn=conn, cur=cur)
    
    return jsonify(result[0])

def sort_posts(data):
    post_id_list = data['list']
    conn, cur = Connect_to_db('Posts', need_dicts_factory=True)
    conn.execute('ATTACH DATABASE "vote.db" as vote')
    sorted_posts = cur.execute('''
                            SELECT * 
                            FROM Posts
                            JOIN vote.Votes
                                ON Posts.id = vote.Votes.post_id
                            WHERE Posts.id IN {}
                            ORDER BY karma DESC;
                            '''.format(tuple(post_id_list))).fetchall()
    
    Close_db(conn, cur)
    return jsonify(sorted_posts)

def top_posts():
    conn, cur = Connect_to_db('Posts', need_dicts_factory=True)
    conn.execute('ATTACH DATABASE "vote.db" as vote')

    top_posts = cur.execute('''
                SELECT * 
                FROM Posts
                JOIN vote.Votes 
                    ON Posts.id = vote.Votes.post_id
                ORDER BY vote.Votes.karma DESC 
                LIMIT 20;
                ''').fetchall()

    Close_db(conn, cur)
    results = {}
    results['posts'] = top_posts
    return jsonify(results)

@app.route('/Vote', methods=["GET", "PUT", "POST"])
def Vote():
    data = request.get_json()
    print('Command = {}'.format(data['command']))
    command = data['command']
    if request.method == 'PUT':
        if command == 'upvote':
            return voting(data['post_id'], True)
        elif command == 'downvote':
            return voting(data['post_id'], False)

    elif request.method == 'POST':
        if command == 'sort':
            return sort_posts(data)

    elif request.method == 'GET':
        if command == 'report':
            return report(data['post_id'])
        
        elif command == 'top':
            return top_posts()

@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404 NOT FOUND (i think)</h1><p>{}</p>'''.format(e), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
