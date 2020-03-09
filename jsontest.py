from flask import Flask, request

app = Flask(__name__)

# curl -i -X POST http://127.0.0.1:5000/post -d '{"post-title":"wow", "post-body":"F"}' -H 'Content-Type: application/json'
@app.route('/post', methods=['POST'])
def post_route():
    if request.method == 'POST':

        data = request.get_json()

        print('Data Received: "{}"'.format(data['post-title']))
        return "Request Processed.\n"

app.run()