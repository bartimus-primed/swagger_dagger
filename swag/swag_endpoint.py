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
        self.methods = []
        self.debug = debug
        for k, v in raw_json.items():
            self.methods.append(SE_METHOD(
                self.host, k.upper(), v, self.conn_type, self.endpoint_location, self.debug))

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

    def list_methods(self):
        dict_of_methods = {}
        for method in self.methods:
            dict_of_methods[method.method] = method.list_parameters()
        return dict_of_methods

    def get_method(self, method_type):
        for method in self.methods:
            if method.method == method_type:
                return method
        return False
