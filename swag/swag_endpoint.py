from swag.swag_types import SE_METHOD
import json

"""
    The swag endpoint keeps track of the valid methods

    Returns:
        SwagEndpoint: An object that allows you to test connection, attack, or fuzz
    """


class SwagEndpoint:
    def __init__(self, host, raw_json, endpoint_addr):
        self.host = host
        self.conn_type = endpoint_addr.split("://")[0]
        self.endpoint_location = "/" + "/".join(endpoint_addr.split("/")[3:])
        self.endpoint_get = None
        self.endpoint_post = None
        self.methods = []
        for k, v in raw_json.items():
            match(k):
                case "get":
                    self.endpoint_get = SE_METHOD(
                        self.host, "GET", v, self.conn_type, self.endpoint_location)
                    self.methods.append(self.endpoint_get)
                case "post":
                    self.endpoint_post = SE_METHOD(
                        self.host, "POST", v, self.conn_type, self.endpoint_location)
                    self.methods.append(self.endpoint_post)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()

    def test_connections(self):
        for method in self.methods:
            method.test_endpoint_connection()

    def check_successful(self):
        for method in self.methods:
            if method.successful:
                return method.successful_response
