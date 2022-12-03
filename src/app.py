import os
import sys
from pathlib import Path
import sys

from flask import Flask
from flask_cors import CORS
import awsgi

sys.path.append(str(Path(__file__).parent))
from flask_json_encoder import FlaskJSONEncoder  # noqa: E731
from controllers import (
    health_check,
    count,
    user_redirect,
)  # noqa: E731

# proxy使用時のWarningの非表示
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

config_type = {
    "local": "config.Local",
    "development": "config.Development",
    "staging": "config.Staging",
    "production": "config.Production",
    "test": "config.Test",
}

app = Flask(__name__)
app.json_encoder = FlaskJSONEncoder
CORS(app, support_credentials=True)

# 設定ファイルの読み込み
app.config.from_object(config_type.get(os.getenv("FLASK_APP_ENV", "local")))
# loggerの設定
logger = app.logger
logger.setLevel(app.config["LOG_LEVEL"])

app.register_blueprint(health_check.app)
app.register_blueprint(count.app)
app.register_blueprint(user_redirect.app)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)


def lambda_handler(event, context):
    return awsgi.response(app, event, context)
