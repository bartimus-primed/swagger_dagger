import json
import queue
from urllib.request import urlopen
from swag.swag_endpoint import SwagEndpoint
from enum import Enum
from http.client import HTTPConnection, HTTPSConnection
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


"""

SwagManager is the top level class to allow easy interaction with an entire website.
SwagManager should contain multiple SwagEndpoints associated with the site.
If you only have a single endpoint you are testing then creating a SwagEndpoint by iteself is more efficient.


Returns:
    SwagManager: Allows easy managing of entire site with multiple endpoints.
"""


class SwagManager:
    def __init__(self, endpoint, debug=False):
        self._parse_queue = queue.Queue()
        self.endpoint_data = None
        self.base_api = None
        self.host = None
        self.swagger = None
        self.info = None
        self.tags = None
        self.paths = None
        self.definitions = None
        self.open_endpoints = []
        self.endpoints = {}
        self.endpoint = endpoint
        self.desired_protocol = self.endpoint.split("://")[0].lower()
        self.debug = debug
        self.get_swag_endpoint_data()
        self.parse_swagger_json()

    # Read the json endpoint. I need to add a brute force checker for common locations.
    def get_swag_endpoint_data(self):
        try:
            with urlopen(self.endpoint, timeout=3) as swag_conn:
                self.endpoint_data = json.load(swag_conn)
        except:
            # This is incase just the web platform is given
            # TODO: need to make this work better. Probably need to scrape the page to get the js file that loads the endpoint data.
            # Populate all the SwagManager Properties that will be needed to attack
            connection = None
            url = self.endpoint.split("://")[1].lower().split("/")[0]
            connection_point = "/" + \
                "/".join(self.endpoint.split(":")[2].split("/")[1:])
            match(self.desired_protocol):
                case "http":
                    connection = HTTPConnection(url, timeout=1)
                case "https":
                    connection = HTTPSConnection(url, timeout=1)
                case _:
                    exit("Did you forget to put http/https?")
            connection.request("GET", connection_point, encode_chunked=True,
                               headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"})
            resp = connection.getresponse()
            print(resp.read())
            print(resp.geturl())
            if str(resp.status) == "200":
                print(resp.read().decode("utf8"))

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
                                                                 path_value, self.make_endpoint(path_name), self.debug)
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

    def detect_open_endpoints(self):
        for endpoint_name, endpoint in self.endpoints.items():
            success = endpoint.check_successful()
            if success:
                if self.debug:
                    print(
                        f"Endpoint: {endpoint_name} seems to be open\n\tresponse: {success}")
                self.open_endpoints.append(endpoint)

    def print_open_endpoints(self, only_show_parameters=False):
        for endpoint in self.open_endpoints:
            if only_show_parameters:
                for method in endpoint.methods:
                    if method.parameters:
                        for entry in method.parameters:
                            print(entry)
            else:
                print(endpoint)
