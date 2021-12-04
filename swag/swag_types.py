import json
from http.client import HTTPConnection, HTTPSConnection
"""
Swag types is broken off so there is an easier way to fuzz the parameters. We can do all the checks inside here as well as generate new outputs.
If someone wants to write special fuzz cases or anything, they can essentially add them as a class and add that to a swag_endpoint's methods list
"""

"""
Currently just a placeholder class, until I can integrate it.
"""
class SwagTypes:
    def __init__(self, parameter_name, parameter_type):
        self.parameter_name = parameter_name
        """
        TODO: We will generate the _described_type from the Descriptions endpoint
        """
        self._described_type = parameter_type

    def generate_fuzz(self):
        # Create the fuzzy stuffing
        pass


class SE_METHOD:
    def __init__(self, host, method, raw_json, conn_type, endpoint_location):
        self.host = host
        self.method = method
        self.conn_type = conn_type
        self.endpoint_location = endpoint_location
        self.send_type = None
        self.parameters = None
        self.receive_type = None
        self.summary = None
        self.responses = {}
        self.successful = False
        self.successful_response = False
        self.build_data(raw_json)

    def build_data(self, details):
        for k, v in details.items():
            match(k):
                case "consumes":
                    self.send_type = v
                case "parameters":
                    self.parameters = v
                case "produces":
                    self.receive_type = v
                case "summary":
                    self.summary = v
                case "responses":
                    for sub_k, sub_v in v.items():
                        if sub_v["description"] is not None:
                            self.responses[sub_k] = SE_RESPONSE(
                                sub_k, sub_v["description"])

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()

    def test_endpoint_connection(self):
        connection = None
        match(self.conn_type.lower()):
            case "http":
                connection = HTTPConnection(self.host, timeout=1)
            case "https":
                connection = HTTPSConnection(self.host, timeout=1)
            case _:
                print("unsupported method. (for right now)")
                return
        if connection is not None:
            connection.request(
                self.method, self.endpoint_location)
            resp = connection.getresponse()
            if str(resp.status) == "200":
                self.successful = True
                try:
                    self.successful_response = json.loads(
                        resp.read().decode("utf8").replace("'", '"'))
                except:
                    self.successful_response = resp.read().decode("utf8")
            connection.close()


class SE_RESPONSE:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()
