from abc import ABC, abstractclassmethod
import json
import re
"""
    Swag Manipulator's allow a SE_METHOD to fuzz it's parameters. Essentially you can assign maniplulators
    to the SE_METHOD and then call SE_METHOD.fuzz() which will generator a manipulation of the parameters
    and send them to the endpoint.
    Creating a new manipulator should inherit the SwagManipulator parent class and implement the abstract class functions
    1. generate
    2. permutate
"""

URL_PARAMETER = re.compile('{(.*?)}')


class SwagManipulator(ABC):

    def __init__(self):
        self.PATH_REPLACEMENT = "{" + self.parameter_name + "}"
        self.parameter_queue = []

    @abstractclassmethod
    def generate(self):
        pass

    @abstractclassmethod
    def permutate(self, original_value):
        pass

    def add_to_queue(self, parameter):
        self.parameter_queue.append(parameter)

    def get_from_queue(self):
        if len(self.parameter_queue) > 0:
            return self.parameter_queue.pop()
        return self.default_value

    def replace_parameter(self, url_string):
        if url_string.__contains__(self.PATH_REPLACEMENT):
            return url_string.replace(self.PATH_REPLACEMENT, self.get_from_queue())
        if self.parameter_location == "query":
            if "?" not in url_string:
                return f"{url_string}?{self.parameter_name}={self.get_from_queue()}"
            else:
                return f"{url_string}&{self.parameter_name}={self.get_from_queue()}"
        return url_string

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()
