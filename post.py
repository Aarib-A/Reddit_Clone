from database import *
from flask import Flask, jsonify, request, redirect, url_for, abort, Response
from datetime import datetime


import post_faker


app = Flask(__name__)
app.config["DEBUG"] = True

# SUBMIT A POST
def submit(data):
    print(data)
    post_id = data['post_id']
    user_id = data['user_id']
    community = data['community']
    date = str(datetime.utcnow())
    post_title = data['post_title']
    post_body = data['post_body']


    post_faker.create_ze_Post(post_id,user_id, community, date, \
             post_title, post_body)

    status_code = Response(status=201)
    return status_code

# RETRIEVE COMMUNITY POSTS
def retrieve_community_posts(community):
    return jsonify(post_faker.get_all_ZE_post(20, community))

# RETRIEVE ALL POSTS
def retrieve_all_posts():
    return jsonify(post_faker.get_all_ZE_post(20))

# RETRIEVE A SINGLE POST 
def retrieve_post_content(post_id):
    # return jsonify(post_faker.get_ze_Post(post_id))
    return jsonify(post_faker.get_ze_Post_FIXED(post_id))



# DELETING A POST 
def delete_post(post_id):
    post_faker.delete_ze_Post(post_id)
    
    status_code = Response(status=200)
    return status_code 

# RSS friendly
def RSS_friendly(posts):
    whole_dict = {}
    whole_dict['posts'] = posts
    return whole_dict

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




