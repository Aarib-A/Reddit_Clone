
#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Posts')

with open("dataload.json") as json_file:
    movies = json.load(json_file, parse_float = decimal.Decimal)
    for movie in movies:
        id = int(movie['id'])
        user_id = movie['user_id']
        community = movie['community']
        date = movie['date']
        post_title = movie['post_title']
        post_body = movie['post_body']

        print("Adding post:", id, community, date)

        table.put_item(
           Item={
            #    'year': year,
            #    'title': title,
            #    'info': info,
                'id': id,
                'user_id': user_id,
                'community': community,
                'date': date,
                'post_title': post_title,
                'post_body': post_body
            }
        )
