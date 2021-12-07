from swag.swag_manipulator import SwagManipulator
"""
    To ensure we can send parameters to endpoints, this DefaultManipulator returns a default value for the parameter
"""


class DefaultManipulator(SwagManipulator):
    def __init__(self, parameter_name, parameter_type, parameter_location, default_value):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.default_value = default_value
        self.parameter_location = parameter_location
        super().__init__()
        self.generate()

    def generate(self):
        self.add_to_queue(self.default_value)

    def permutate(self, original_value):
        return self.get_rules()

    def get_rules(self):
        return "DEFAULTRULE"
