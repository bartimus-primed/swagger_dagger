import json
import queue
from urllib.request import urlopen
from swag.swag_endpoint import SwagEndpoint
from enum import Enum


class RESULT(Enum):
    NO = 0
    YES = 1,
    MAYBE = 2,


class SwagManager:
    def __init__(self, endpoint):
        self._parse_queue = queue.Queue()
        self.endpoint_data = None
        self.base_api = None
        self.host = None
        self.swagger = None
        self.info = None
        self.tags = None
        self.paths = None
        self.definitions = None
        self.endpoints = {}
        self.endpoint = endpoint
        self.desired_protocol = self.endpoint.split("://")[0]
        self.get_swag_endpoint_data()
        self.parse_swagger_json()

    # Read the json endpoint. I need to add a brute force checker for common locations.
    def get_swag_endpoint_data(self):
        with urlopen(self.endpoint, timeout=3) as swag_conn:
            self.endpoint_data = json.load(swag_conn)

    # Populate all the SwagManager Properties that will be needed to attack
    def parse_swagger_json(self):
        for k, v in self.endpoint_data.items():
            match(k):
                case "swagger":
                    self.swagger = v
                case "host":
                    self.host = v
                case "basePath":
                    self.base_api = v
                case "tags":
                    self.tags = v
                case "paths":
                    self.paths = v
                    for path_name, path_value in v.items():
                        self.endpoints[path_name] = SwagEndpoint(self.host,
                                                                 path_value, self.make_endpoint(path_name))
                    pass
                case "definitions":
                    self.definitions = v
                    # self.parse_definitions("token")
                case _:
                    pass

    def pre_endpoint(self):
        return f"{self.host}{self.base_api}"

    def make_endpoint(self, endpoint):
        # Get rid of double forward slashes if they occur, should still work with them, but I don't like it.
        if self.base_api[-1] == "/" and endpoint[0] == "/":
            return f"{self.desired_protocol}://{self.host}{endpoint}"
        return f"{self.desired_protocol}://{self.host}{self.base_api}{endpoint}"

    def test_connections(self):
        for endpoint_name, endpoint in self.endpoints.items():
            endpoint.test_connections()

    def check_successful(self):
        for endpoint_name, endpoint in self.endpoints.items():
            success = endpoint.check_successful()
            if success is not None:
                print(f"Endpoint: {endpoint_name}, response: {success}")
