import datetime
from flask import Blueprint, jsonify, current_app, logging, request
from const.status_code import SUCCESS_OK, CLIENT_BAD_REQUEST
import random
from flask import current_app
import boto3
from boto3.dynamodb.conditions import Key


app = Blueprint("count", __name__)
g_dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
limit_target_number = 5


@app.route("/count/<string:user>", methods=["GET"])
def get_count(user):
    """
    カウントの取得
    """
    logger = logging.create_logger(current_app)
    logger.info("get_count")
    logger.info("******** headers ***********")
    logger.info(request.headers)
    logger.info("******** args ***********")
    logger.info(request.args)
    logger.info(user)
    stage = current_app.config.get("STAGE", "")
    # ローカル環境ではない場合にユーザーを取得する
    if stage != "local":
        table = g_dynamodb.Table("url_access")
        # ユーザー情報を取得する
        items = table.query(
            KeyConditionExpression=Key("connection_id").eq(user),
            ScanIndexForward=False,
            Limit=1,
        )
        # コネクションが存在しない場合はエラーとする
        if items["Count"] == 0:
            return (
                jsonify({"message": "not found connectId"}),
                CLIENT_BAD_REQUEST,
            )

        url = items["Items"][0]["url"]
        user_access_time = int(items["Items"][0]["time"])
        url_time_index = "url-time-index"
        # 1分前よりアクセスが前であればリダイレクトを許可する
        # target_time_at = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
        # target_time = int(target_time_at.timestamp())
        # NOTE デモ用に30秒とする
        target_time_at = datetime.datetime.utcnow() - datetime.timedelta(seconds=30)
        target_time = int(target_time_at.timestamp())
        if target_time > user_access_time:
            return (
                jsonify({"count": 0}),
                SUCCESS_OK,
            )
        accesses_items = table.query(
            IndexName=url_time_index,
            KeyConditionExpression=Key("url").eq(url) &
            Key("time").between(target_time, user_access_time),
            ScanIndexForward=False,
            Limit=10000,
        )
        logger.info(accesses_items)
        # アクセス制限以下のレコードであればリダイレクトを許可する(取り急ぎ5)
        if accesses_items["Count"] - limit_target_number <= 0:
            return (
                jsonify({"count": 0}),
                SUCCESS_OK,
            )

        # 自身のカウントは除く
        return (
            jsonify({"count": accesses_items["Count"] - limit_target_number}),
            SUCCESS_OK,
        )

    # ローカルでは乱数にする
    count_number = random.randrange(5)
    return (
        jsonify({"count": count_number}),
        SUCCESS_OK,
    )
