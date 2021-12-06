from abc import ABC, abstractclassmethod
import json
"""
    Swag Manipulator's allow a SE_METHOD to fuzz it's parameters. Essentially you can assign maniplulators
    to the SE_METHOD and then call SE_METHOD.fuzz() which will generator a manipulation of the parameters
    and send them to the endpoint.
    Creating a new manipulator should inherit the SwagManipulator parent class and implement the abstract class functions
"""


class SwagManipulator(ABC):

    def __init__(self, parameter_name, parameter_type, default_value):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.default_value = default_value

    @abstractclassmethod
    def generate(self):
        pass

    @abstractclassmethod
    def get_rules(self):
        pass

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()
