import base64
import json

from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("utf-8")
        return json.JSONEncoder.default(self, o)
