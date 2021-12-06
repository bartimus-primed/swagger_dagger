import json
from http.client import HTTPConnection, HTTPSConnection
from re import split
from swag.manipulators import *
from swag.manipulators.Default import DefaultManipulator

"""
Swag types is broken off so there is an easier way to interact with each API method.
We can do all the checks inside here as well as generate new outputs.
The SwagEndpoint and SwagManager eventually call the SE_METHOD (short for SwaggerEndpoint_Method) class.
In essence SwagEndpoint and SwagManagers are simply batch managers which allow multiple things to happen
on individual SE_METHODs.
"""


class SE_METHOD:
    def __init__(self, host, method, raw_json, conn_type, endpoint_location, debug=False):
        self.host = host
        self.method = method
        self.conn_type = conn_type
        self.endpoint_location = endpoint_location
        self.fuzzed_endpoint_location = None
        self.send_type = None
        self.parameters = None
        self.all_parameters = []
        self.optional_parameters = []
        self.required_parameters = []
        self.receive_type = None
        self.summary = None
        self.responses = {}
        self.successful = False
        self.successful_response = False
        self.debug = debug
        self.build_data(raw_json)

    def build_data(self, details):
        for k, v in details.items():
            match(k):
                case "consumes":
                    self.send_type = v
                case "parameters":
                    self.parameters = v
                    self.parse_parameter_data()
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
                if self.debug:
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

    def generate_parameter_url(self):
        generation_path = self.endpoint_location
        for param in self.all_parameters:
            match(param.location):
                # At the end of the current url host.com/path/to?param=""
                case "query":
                    param_generation = "PARAM_VALUE"
                    for gen in param.manipulators:
                        param_generation = gen.generate()
                    if "?" not in generation_path:
                        param_query = f"?{param.name}={param_generation}"
                    else:
                        param_query = f"&{param.name}={param_generation}"
                    generation_path += param_query
                    self.fuzzed_endpoint_location = generation_path
                # Needs to be added to request body
                case "body":
                    pass
                # needs to be replaced in the path host.com/REPLACED/path/to
                case "path":
                    if param.name in generation_path:
                        param_generation = "NEW_VALUE"
                        for gen in param.manipulators:
                            param_generation = gen.generate()
                        replacer = "{" + param.name + "}"
                        generation_path = generation_path.replace(
                            replacer, param_generation)
                    self.fuzzed_endpoint_location = generation_path
        if self.debug:
            print(self.fuzzed_endpoint_location)

    def parse_parameter_data(self):
        if self.parameters is not None:
            for parameter in self.parameters:
                param = SE_PARAMETER(parameter)
                if param.required:
                    self.required_parameters.append(param)
                else:
                    self.optional_parameters.append(param)
            self.all_parameters += self.required_parameters
            self.all_parameters += self.optional_parameters

    def add_manipulator(self, new_manipulator):
        self.manipulators.append(new_manipulator)

    def run_manipulators(self):
        for mani in self.manipulators:
            mani.generate()


class SE_RESPONSE:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()


class SE_PARAMETER:

    def __init__(self, data, debug=False):
        self.name = None
        self.location = None
        self.description = None
        self.required = None
        self.default = None
        self.format = None
        self.type_of = None
        self.debug = debug
        self.manipulators = []
        for d in data.keys():
            match(d):
                case "name":
                    self.name = data["name"]
                case "in":
                    self.location = data["in"]
                case "description":
                    self.description = data["description"]
                case "required":
                    self.required = data["required"]
                case "default":
                    self.default = data["default"]
                case "format":
                    self.format = data["format"]
                case "type":
                    self.type_of = data["type"].lower()
        self.assign_default_manipulator()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()

    def assign_default_manipulator(self):
        if self.type_of is None:
            return
        match(self.type_of):
            case "string":
                self.manipulators.append(
                    StringManipulator(self.name, self.type_of, self.default))
            case "integer":
                self.manipulators.append(
                    IntegerManipulator(self.name, self.type_of, self.default))
            case "boolean":
                self.manipulators.append(
                    BooleanManipulator(self.name, self.type_of, self.default))
            case "array":
                self.manipulators.append(
                    ArrayManipulator(self.name, self.type_of, self.default))
            case _:
                if self.default is not None:
                    if self.debug:
                        print(f"No Manipulator implemented for {self.type_of}")
                        print(
                            "Identified default value assigning default manipulator")
                    self.manipulators.append(DefaultManipulator(
                        self.name, self.type_of, self.default))
