from decimal import Decimal
from datetime import date, datetime

from flask.json import JSONEncoder


class FlaskJSONEncoder(JSONEncoder):
    def default(self, obj):
        # TODO: 足りないものが合ったら都度足していく
        if isinstance(obj, Decimal):
            if int(obj) == obj:
                return int(obj)
            else:
                return float(obj)
        if isinstance(obj, bytes):
            return obj.decode()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return super().default(obj)
