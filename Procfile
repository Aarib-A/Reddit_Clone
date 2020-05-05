DYNO: java -Djava.library.path=./databases/DynamoDBLocal_lib -jar databases/DynamoDBLocal.jar -sharedDb
REDIS: redis-server
VOTE: gunicorn3 vote:app
POST: gunicorn3 post:app
RSS: gunicorn RSSWS:app

