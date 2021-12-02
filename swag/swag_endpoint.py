from swag.swag_types import SE_RESPONSE, SE_GET, SE_POST
import json

"""
    The swag endpoint keeps track of the valid methods

    Returns:
        SwagEndpoint: An object that allows you to test connection, attack, or fuzz
    """


class SwagEndpoint:
    def __init__(self, raw_json):
        self.endpoint_get = None
        self.endpoint_post = None
        self.methods = []
        for k, v in raw_json.items():
            match(k):
                case "get":
                    self.endpoint_get = SE_GET(v)
                    self.methods.append(self.endpoint_get)
                case "post":
                    self.endpoint_post = SE_POST(v)
                    self.methods.append(self.endpoint_post)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()
