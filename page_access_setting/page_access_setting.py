import base64
import datetime
import logging
import os
import random
import boto3
from time import time
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO")))
g_dynamodb = boto3.resource("dynamodb", region_name='us-east-1')


def lambda_handler(event, context):
    logger.info(event)
    # 現在のUNIX時間を取得
    unix_time = int(time())
    # TTLの設定(2分後とする)
    after_1days_from_now = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    expire = int(after_1days_from_now.timestamp())
    request = event['Records'][0]['cf']['request']
    connection_id = event['Records'][0]['cf']['config']["requestId"]
    table = g_dynamodb.Table("url_access")
    table.put_item(
        Item={"connection_id": connection_id,
              "url": request['uri'], "time": unix_time, "expire": expire}
    )
    logger.info("normal request")
    url_time_index = "url-time-index"
    # 1分以内のアクセスを取得するようにする
    target_time_at = datetime.datetime.utcnow() - datetime.timedelta(seconds=30)
    target_time = int(target_time_at.timestamp())
    items = table.query(
        IndexName=url_time_index,
        KeyConditionExpression=Key("url").eq(request['uri']) &
        Key("time").gte(target_time),
        ScanIndexForward=False,
        Limit=10000,
    )
    logger.info(items)
    logger.info(items["Count"])
    # 特定の回数以上アクセスがあった場合はsorry Pageにリダイレクトする(今の所5回までとする)
    if items["Count"] > 5:
        # Definition
        redirect_protocol = "https"
        redirect_domain = "d2u31az4sadte8.cloudfront.net"
        # redirect_uri = redirect_protocol + '://' + redirect_domain + request['uri']
        redirect_uri = redirect_protocol + '://' + \
            redirect_domain + '/' + '?connect=' + connection_id
        response = {
            'status': '302',
            'statusDescription': 'Found',
            'headers': {
                'location': [{
                    'key': 'Location',
                    'value': redirect_uri
                }]
            }
        }
        logger.info("redirect uri")
        return response

    return request
