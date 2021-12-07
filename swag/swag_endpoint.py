from swag.swag_types import SE_METHOD
import json

"""
    The swag endpoint keeps track of the valid SE_METHODS. A Single endpoint can have multiple
    SE_METHODS, though I think it's better to only have one for each http method that is supported.
    e.g.
    PUT -> SE_METHOD
    GET -> SE_METHOD
    POST -> SE_METHOD

    Returns:
        SwagEndpoint: An object that allows you to test connection, attack, or fuzz
    """


class SwagEndpoint:
    def __init__(self, host, raw_json, endpoint_addr, debug=False):
        self.host = host
        self.conn_type = endpoint_addr.split("://")[0]
        self.endpoint_location = "/" + "/".join(endpoint_addr.split("/")[3:])
        self.endpoint_get = None
        self.endpoint_post = None
        self.methods = []
        self.debug = debug
        for k, v in raw_json.items():
            self.endpoint_post = SE_METHOD(
                self.host, k.upper(), v, self.conn_type, self.endpoint_location, self.debug)
            self.methods.append(self.endpoint_post)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()

    def test_connections(self):
        for method in self.methods:
            method.test_endpoint_connection()

    def get_parameters(self):
        for method in self.methods:
            if method.parameters is not None:
                if self.debug:
                    print(method.parameters)

    def check_successful(self):
        for method in self.methods:
            if method.successful:
                return method.successful_response

    def print_open_methods(self, only_show_parameters=False):
        for method in self.methods:
            print(method)
