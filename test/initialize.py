from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


table = dynamodb.create_table(
    TableName='Posts',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'  #Partition key
        },
        # {
        #     'AttributeName': 'community',
        #     'KeyType': 'RANGE'  #Sort key
        # }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        }
        # },
        # {
        #     'AttributeName': '',
        #     'AttributeType': 'S'
        # },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)



# aws dynamodb list-tables --endpoint-url http://localhost:8000