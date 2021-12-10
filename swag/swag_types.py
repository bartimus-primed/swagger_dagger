import json
from http.client import HTTPConnection, HTTPSConnection
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
        self.last_response = False
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
                                sub_k, sub_v)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()

    def test_endpoint_connection(self, print_response=False, fuzzed=False):
        connection = None
        if fuzzed and print_response:
            self.generate_parameter_url()
            print(
                f"Fuzzing {self.method} request {self.endpoint_location} with these parameters: {self.fuzzed_endpoint_location}")
        match(self.conn_type.lower()):
            case "http":
                connection = HTTPConnection(self.host, timeout=1)
            case "https":
                connection = HTTPSConnection(self.host, timeout=1)
            case _:
                if self.debug:
                    print("unsupported protocol. (for right now)")
                return
        if connection is not None:
            if fuzzed:
                connection.request(self.method, self.fuzzed_endpoint_location)
            else:
                connection.request(self.method, self.endpoint_location)
            resp = connection.getresponse()
            resp_status = str(resp.status)
            if resp.getheader("content-type") is not None:
                resp_content_type = resp.getheader("content-type").strip()
            else:
                resp_content_type = ""
            if print_response:
                print(f"Response Code: {resp_status}")
            if resp_status == "200" or resp_content_type == "application/json":
                self.successful = True
                try:
                    self.successful_response = json.loads(
                        resp.read().decode("utf8").replace("'", '"'))
                except:
                    self.successful_response = resp.read().decode("utf8")
                self.last_response = self.successful_response
                if print_response:
                    print(self.successful_response)
            else:
                try:
                    self.last_response = json.loads(
                        resp.read().decode("utf8").replace("'", '"'))
                except:
                    self.last_response = resp.read().decode("utf8")
                if print_response:
                    print(self.last_response)
            connection.close()

    def generate_parameter_url(self):
        self.fuzzed_endpoint_location = self.endpoint_location
        for param in self.all_parameters:
            if param.manipulator is not None:
                self.fuzzed_endpoint_location = param.manipulator.replace_parameter(
                    self.fuzzed_endpoint_location)
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

    def list_parameters(self):
        list_of_parameters = []
        for param in self.all_parameters:
            list_of_parameters.append(param.name)
        return list_of_parameters

    def get_parameter(self, parameter_number):
        if parameter_number < len(self.all_parameters):
            return self.all_parameters[parameter_number]
        return False


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
        self.manipulator = None
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
            self.type_of = "null"
        match(self.type_of):
            case "string":
                self.manipulator = StringManipulator(
                    self.name, self.type_of, self.location, self.default)
            case "integer":
                self.manipulator = IntegerManipulator(
                    self.name, self.type_of, self.location, self.default)
            case "boolean":
                self.manipulator = BooleanManipulator(
                    self.name, self.type_of, self.location, self.default)
            case "array":
                self.manipulator = ArrayManipulator(
                    self.name, self.type_of, self.location, self.default)
            case _:
                if self.debug:
                    print(f"No Manipulator implemented for {self.type_of}")
                    print("Identified default value assigning default manipulator")
                if self.default is not None:
                    self.manipulator = DefaultManipulator(
                        self.name, self.type_of, self.location, self.default)
                else:
                    self.manipulator = NullManipulator(
                        self.name, self.type_of, self.location)

    def describe(self):
        return f"\tlocation: {self.location}\n\tdescription: {self.description}\n\trequired: {self.required}\n\tdefault value: {self.default}\n\tformat: {self.format}\n\ttype: {self.type_of}\n\tassigned manipulators: {self.manipulator.get_name()}\n"
