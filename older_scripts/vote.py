from flask import Flask, jsonify, request, Response, abort 
import redis
import dateutil.parser

from hot_alg import hot
from operator import itemgetter, attrgetter
from post_faker import get_all_ZE_post_id_s, get_ze_posts_based_on_list, get_all_ZE_post

app = Flask(__name__)
app.config["DEBUG"] = True

# Redis Database
r = redis.Redis(decode_responses=True)

# post id prefix for redis db
def prefix(post_ids):
    for i in range(0, len(post_ids)):
        post_ids[i] = 'post_id:' + str(post_ids[i])
    return post_ids

# get upvotes and downvotes for multiple posts
def get_ups_downs(post_ids): 
    post_ids = prefix(post_ids)

    with r.pipeline() as pipe:
        pipe.multi()
        for post in post_ids:
            pipe.hmget(post, 'upvote', 'downvote')
        return pipe.execute()

# add upvotes and downvotes to dataset
def join_tables(posts):
    post_ids = []
    for post in posts:
        post_ids.append(post['id'])
    ups_downs = get_ups_downs(post_ids)

    if(len(ups_downs) != len(posts)):
        print('Votes Array different from Posts Array')

    for i in range(0, len(posts)):
        posts[i]['upvote'] = ups_downs[i][0]
        posts[i]['downvote'] = ups_downs[i][1]

    return posts

# Create new entry in redis
def create_new_vote(post_id):
    # Check if post id exists
    if r.exists(f'post_id:{post_id}'):
        print(f'Post Id: {post_id} does exists already')
        status_code = Response(status=409)
        return status_code

    vote = {f'post_id:{post_id}': {
        "post_id": post_id,
        "karma" : 1,
        "upvote": 1,
        "downvote": 0
    }}
    
    with r.pipeline() as pipe:
        pipe.multi()
        for key, val in vote.items():
            pipe.hmset(key, val)
            pipe.sadd('posts', key)
        pipe.execute()

    print(r.hgetall(f'post_id:{post_id}'))
    status_code = Response(status=201)
    return status_code

# DONE, MAY NEED EXTRA SECURITY , CHECK IF KEY EXISTS
def voting(post_id, is_upvote):
    # Check if post id exists
    if not r.exists(f'post_id:{post_id}'):
        print(f'Post Id: {post_id} does not exist')
        status_code = Response(status=409)
        return status_code

    # Voting
    with r.pipeline() as pipe:
        while True:
            try: 
                pipe.watch(f'post_id:{post_id}')
                pipe.multi()
                if is_upvote:
                    pipe.hincrby(f'post_id:{post_id}', 'upvote', 1)
                    pipe.hincrby(f'post_id:{post_id}', 'karma', 1)
                else:
                    pipe.hincrby(f'post_id:{post_id}', 'downvote', 1)
                    pipe.hincrby(f'post_id:{post_id}', 'karma', -1)
                pipe.execute()
                break
            except redis.WatchError:
                # Conflict Error
                print(f'WatchError for Post_id: {post_id}')
                status_code = Response(status=409)
                return status_code

    status_code = Response(status=200)
    return status_code

# return single row in Votes db 
def report(post_id):
    post_id = str(post_id)
    report = r.hgetall(f'post_id:{post_id}')
    if not bool(report):
        status_code = Response(status=404)
        return status_code
    # return jsonify(report)
    return report

# sort posts 
def sort_posts(data):
    post_id_list = prefix(data)
    
    sorted_posts = None

    with r.pipeline() as pipe:
        pipe.multi()
        pipe.sadd('temp_posts', *post_id_list)
        pipe.sort(name='temp_posts', by='*->karma', get='*->post_id', desc=True) 
        pipe.delete('temp_posts')
        sorted_posts = pipe.execute()[1] #get the 2nd output in the pipe
    
    return sorted_posts

# Returns the top 25 post_ids 
def top_posts():
    sorted_post_ids = r.sort(name='posts', start=0, num=25, by='*->karma', get='*->post_id', desc=True)
    sorted_post_ids = [int(i) for i in sorted_post_ids]

    top_posts = get_ze_posts_based_on_list(sorted_post_ids)
    top_posts = join_tables(top_posts)
    return jsonify(top_posts)

# Top Community Posts **************
def top_community_posts(community):
    print(type(community))
    # get the post details
    post_ids = get_all_ZE_post_id_s(community=community)

    # sort post ids by karma
    sorted_post_ids = sort_posts(post_ids)
    sorted_post_ids = [int(i) for i in sorted_post_ids]

    # get post from dynamodb based on sorted post ids 
    sorted_posts = get_ze_posts_based_on_list(sorted_post_ids)

    # join the tables 
    sorted_posts = join_tables(sorted_posts)
    # return sorted posts
    return jsonify(sorted_posts)
     

# Hot Post *************
def hot_posts():
    posts = get_all_ZE_post(200)
    posts = join_tables(posts)

    for post in posts:
        post['hot'] = hot(int(post['upvote']), int(post['downvote']), dateutil.parser.parse(post['date']))
        
    hot_posts = sorted(posts, key= lambda i: i['hot'], reverse=True)
    return jsonify(hot_posts[:25])

# Delete Vote 
def delete_vote(post_id):
    post_id = f'post_id:{post_id}'
    r.delete(post_id)

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
            return jsonify(sort_posts(data['list']))

    elif request.method == 'GET':
        if command == 'report':
            return report(data['post_id'])
        
        elif command == 'top':
            return top_posts()
        
        elif command == 'hot':
            return hot_posts()

        elif command == 'community':
            return top_community_posts(data['comm_name'])

@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>404 NOT FOUND (i think)</h1><p>{}</p>'''.format(e), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
    # posts = [
    #     {
    #         'id': 666,
    #         'post_body': 'fewofewroewr'
    #     },
    #     {
    #         'id': 667,
    #         'post_body': 'balaoiehrowerew'
    #     }
    # ]
    # print(join_tables(posts))
    # create_new_vote(999)
    # create_new_vote(1202)
    # create_new_vote(1313)
    # create_new_vote(666)
