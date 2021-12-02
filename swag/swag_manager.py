import json
import queue
from urllib.request import urlopen
from swag.swag_endpoint import SwagEndpoint
from pprint import pprint


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
                        self.endpoints[path_name] = SwagEndpoint(
                            path_name, path_value)
                    pass
                case "definitions":
                    self.definitions = v
                    self.parse_definitions("token")
                case _:
                    pass

    def pre_endpoint(self):
        return f"{self.host}{self.base_api}"

    def make_endpoint(self, endpoint):
        # Get rid of double forward slashes if they occur, should still work with them, but I don't like it.
        if self.base_api[-1] == "/" and endpoint[0] == "/":
            return f"{self.desired_protocol}://{self.host}{endpoint}"
        return f"{self.desired_protocol}://{self.host}{self.base_api}{endpoint}"

    def parse_swagger(self):
        pass

    def parse_tags(self):
        pass

    def parse_paths(self):
        pass

    def has(self, this, that):
        this = this.lower()
        that = that.lower()
        return this.__contains__(that)

    def exactly(self, this, that):
        return this.lower() == that.lower()

    def recursive_unwrap(self, current_chain, dictionary):
        current_chain = []
        if isinstance(dictionary, str):
            current_chain.append(dictionary)
        elif isinstance(dictionary, list):
            for idx, value in enumerate(dictionary):
                results = self.recursive_unwrap(current_chain, value)
                if results is not None:
                    current_chain.append(results)
        elif isinstance(dictionary, dict):
            for key, value in dictionary.items():
                results = self.recursive_unwrap(current_chain, value)
                if results is not None:
                    current_chain.append(results)
        if current_chain:
            return current_chain

    def recursive_search(self, type_name, list_obj):
        if isinstance(list_obj, list):
            for i in list_obj:
                self.recursive_search()

    def parse_definitions(self, type_name):
        possible_chains = []
        for key in self.definitions.keys():
            current_chain = self.recursive_unwrap(key, self.definitions)
            possible_chains.append(current_chain)
        candidates = []
        exact = None
        for chain in possible_chains:
            for value in chain:
                new_val = value
                while isinstance(new_val, list):
                    for n in new_val:
                        new_val = n
                        if self.exactly(new_val, type_name):
                            exact = chain
                            break
                        if self.has(new_val, type_name):
                            candidates.append(value)
                            break
        print(exact)
        print(len(candidates))

        # We need to search through the definitions and see if one exists for the argument's type name, if we find that we return it to ensure we fuzz the right data types
