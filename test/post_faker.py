from __future__ import print_function # Python 2/3 compatibility  #https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html
import boto3
import json
import decimal

from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#Create a new post
def create_ze_Post(post_id, user_id, community, date, post_title, post_body):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Posts')

    response = table.put_item(
    Item={
            'id': post_id,
            'user_id': user_id,
            'community': community,
            'date': date,
            'post_title': post_title,
            'post_body': post_body
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))


#Delete an existing post
def delete_ze_Post(post_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Posts')

    print("Starting process of deleting post: {}".format(post_id))

    try:
        response = table.delete_item(
            Key={
                'id': post_id
            }
        # ,
        # ConditionExpression="info.rating <= :val",
        # ExpressionAttributeValues= {
        #     ":val": decimal.Decimal(5)
        # }
    )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        print("DeleteItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))



#Retrieve and existing post
def get_ze_Post(post_id):
    dynamodb = boto3.resource("dynamodb", region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Posts')

    try:
        response = table.get_item(
            Key={
                'id': post_id
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return json.dumps(item, indent=4, cls=DecimalEncoder)


#List the N most Recent posts to a particular community
def get_all_ZE_post(Num, community='any'):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Posts')

    response = table.scan()
    dates_dictionary = {}
    list_of_posts = []

    for i in response['Items']:
        # print(json.dumps(i, cls=DecimalEncoder))
        data = json.dumps(i, cls=DecimalEncoder)
        data = json.loads(data)

        if community == 'any':
            if data['date'] in dates_dictionary:
                dates_dictionary[data['date']].append(data)
            else:
                dates_dictionary[data['date']] = [data]
        else:
            if data['community'] == community:
                if data['date'] in dates_dictionary:
                    dates_dictionary[data['date']].append(data)
                else:
                    dates_dictionary[data['date']] = [data]

    
    loop_count = 0
    for keys in sorted(dates_dictionary, reverse=True):
        
        for list in dates_dictionary[keys]:
            
            # for dicts in list:
                # list_of_posts.append(dicts)
             
            list_of_posts.append(list)
            loop_count += 1
            if loop_count == Num:
                return list_of_posts

    # return list_of_posts
    return json.dumps(list_of_posts)

#list the N most recent posts to any community

def get_all_ZE_post_id_s(community='any'):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Posts')

    response = table.scan()
    dates_dictionary = {}
    list_of_posts = []

    for i in response['Items']:
        # print(json.dumps(i, cls=DecimalEncoder))
        data = json.dumps(i, cls=DecimalEncoder)
        data = json.loads(data)

        if data['community'] == community:
            list_of_posts.append(data['id'])

    return list_of_posts

    
    # loop_count = 0
    # for keys in sorted(dates_dictionary, reverse=True):
        
    #     for list in dates_dictionary[keys]:
            
    #         # for dicts in list:
    #             # list_of_posts.append(dicts)
             
    #         list_of_posts.append(list)

    # # return list_of_posts
    # return json.dumps(list_of_posts)




if __name__ == '__main__':
    post_id = 999
    user_id = 737
    
    community = 'WEEBS'
    import datetime
    date = datetime.datetime.utcnow().isoformat()
    post_title = "Spaget"
    post_body = "somebody touch my spaget!"


    # create_ze_Post(post_id, user_id, community, date, post_title, post_body)


    # print(get_ze_Post(post_id))

    # delete_ze_Post(post_id)

    # data = get_all_ZE_post(40)
    # print(data)
    # print('\n\n\n')
    # print(get_all_ZE_post(5, 'WEEBS'))
    # print(json.dumps(data))


    result = get_all_ZE_post_id_s(community='cool') 
    print(result)
    pass