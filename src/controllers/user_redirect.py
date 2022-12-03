from flask import Blueprint, jsonify, current_app, logging, request
from const.status_code import SUCCESS_OK, CLIENT_BAD_REQUEST
import random
from flask import current_app
import boto3
from boto3.dynamodb.conditions import Key


app = Blueprint("user_redirect", __name__)
g_dynamodb = boto3.resource("dynamodb", region_name='us-east-1')


@app.route("/user-redirect/<string:user>", methods=["GET"])
def get_redirect_url(user):
    """
    リダイレクトURLの取得
    """
    logger = logging.create_logger(current_app)
    logger.info("get_redirect_url")
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

        redirect_url = items["Items"][0]["url"]
        return (
            jsonify({"url": redirect_url}),
            SUCCESS_OK,
        )

    # ローカルの場合はルートディレクトリに遷移
    return (
        jsonify({"url": "/"}),
        SUCCESS_OK,
    )
