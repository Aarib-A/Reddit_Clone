# Reddit Like API

Posting and Voting Microservice

**Preconditional Requirements**:  
    1) Updatable Bash/Linux Environment
    2) Python 2 and 3 installed 

Able to: 

**Retrieves -> returns JSON**

1) Create a Post
2) Retrieve a Certain Post
3) Delete a Post 
4) Retrieve Most Recent Posts from a particular community
5) Retrieve Most Recent Posts from any community

6) Upvote a Post
7) Downvote a Post
8) Retrieve the voting data of a certain post
9) Retrieve the Top Scoring Posts from any community 
10) Retrieve the Top Scoring Posts from a particular community
11) Retrieve the Hot Trending Posts from any community 


**RSS feed -> returns RSS+XML**
1) Retrieve Most Recent Posts from any community
2) Retrieve Most Recent Posts from a particular community
3) Retrieve the Top Scoring Posts from any community
4) Retrieve the Top Scoring Posts from a particular community
5) Retrieve the Hot Trending Posts from any community


**How to Run**  

Install Dependencies
``` 
./dependencies.sh 
```

Run Program 
``` 
./run.sh 
```

**Example: How to**

*Submit a Post*
```
curl -i -X POST 'http://127.0.0.1:8300/Post' -H 'Content-Type: application/json' \
-d '{
    "command":"submit",
    "post_title":"Link to Aiden Pearce",
    "post_id": 1776,
    "post_body": "Could the templars be after him next?",
    "community": "cool",
    "user_id": 47
}'
```

*Retrieve a Post* 
```
curl -i -X GET -H "Content-Type: application/json" \
-d '{"command":"retrieve", "post_id":1776}'  http://127.0.0.1:8300/Post
```

*Delete a Post* 
```
curl -i -X POST -H "Content-Type: application/json" \
-d '{"command":"delete", "post_id":1776}'  http://127.0.0.1:8300/Post
```

*Retrieve Most Recent Posts from a particular community (JSON)*
```
curl -i -X GET -H "Content-Type: application/json" \
-d '{"command": "community", "community": "cool"}'  http://127.0.0.1:8300/Post
```

*Retrieve Most Recent Posts from any community (JSON)*
```
curl -i -X GET -H "Content-Type: application/json" \
-d '{"command":"all"}'  http://127.0.0.1:8300/Post
```

*Upvoting a Post*
```
curl -i -X PUT -H "Content-Type: application/json" -d \
'{"command":"upvote", "post_id":666}'  http://127.0.0.1:8200/Vote
```

*Downvoting a Post*
```
curl -i -X PUT -H "Content-Type: application/json" -d \
'{"command":"downvote", "post_id":666}'  http://127.0.0.1:8200/Vote
```

*Retrieve Voting Data on a Particular Post*
```
curl -i -X GET  -H "Content-Type: application/json" -d \
'{"command":"report", "post_id":666}'  http://127.0.0.1:8200/Vote 
```

*Retrieve Top Posts from a particular community (JSON)*
```
curl -i -X GET  -H "Content-Type: application/json" \
-d '{"command":"community", "comm_name":"cool"}'  http://127.0.0.1:8200/Vote
```

*Retrieve Top Posts from any community (JSON)*
```
curl -i -X GET  -H "Content-Type: application/json"  -d '{"command":"top"}'  http://127.0.0.1:8200/Vote
```

*Retrieve Hot Posts from any community (JSON)* 
```
curl -i -X GET -H "Content-Type: application/json" \
-d '{"command":"hot"}'  http://127.0.0.1:8200/Vote
```



*Retrieve Most Recent Posts from any community (XML)* 
``` 
curl http://127.0.0.1:8400/RSS/recent 
```

*Retrieve Most Recent Posts from a particular community (XML)*
```
curl http://127.0.0.1:8400/RSS/cool/recent
```

*Retrieve the Top Scoring Posts from any community (XML)*
``` 
curl http://127.0.0.1:8400/RSS/top 
```

*Retrieve the Top Scoring Posts from a particular community (XML)*
``` 
curl http://127.0.0.1:8400/RSS/cool/top 
```

*Retrieve the Hot Trending Posts from any community (XML)*
``` 
curl http://127.0.0.1:8400/RSS/hot 
```
