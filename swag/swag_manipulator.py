from abc import ABC, abstractclassmethod, abstractmethod
import json
"""
    Swag Manipulator's allow a SE_METHOD to fuzz it's parameters. Essentially you can assign maniplulators
    to the SE_METHOD and then call SE_METHOD.fuzz() which will generator a manipulation of the parameters
    and send them to the endpoint.
    Creating a new manipulator should inherit the SwagManipulator parent class and implement the abstract class functions
    1. generate
    2. permutate
"""


class SwagManipulator(ABC):

    def __init__(self, parameter_name, parameter_type, parameter_location, default_value=None):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.parameter_location = parameter_location
        self.default_value = default_value
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
        value = self.default_value
        if len(self.parameter_queue) > 0:
            value = self.parameter_queue.pop()
        return value

    def replace_parameter(self, url_string):
        replacement = "{" + self.parameter_name + "}"
        if self.parameter_location == "path":
            if self.parameter_name in url_string:
                url_string = url_string.replace(
                    replacement, self.get_from_queue())
        elif self.parameter_location == "query":
            if "?" not in url_string:
                param_query = f"?{self.parameter_name}={self.get_from_queue()}"
            else:
                param_query = f"&{self.parameter_name}={self.get_from_queue()}"
            url_string += param_query
        return url_string

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()
