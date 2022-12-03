from flask import Blueprint, jsonify, current_app, logging, request
from const.status_code import SUCCESS_OK

app = Blueprint("helth_check", __name__)


@app.route("/health_check", methods=["GET"])
def health_check():
    """
    アプリのコードチェック
    """
    logger = logging.create_logger(current_app)
    logger.info("get_helth_check")
    logger.info("******** headers ***********")
    logger.info(request.headers)
    logger.info("******** args ***********")
    logger.info(request.args)

    return (
        jsonify({}),
        SUCCESS_OK,
    )
