from swag.swag_manipulator import SwagManipulator
"""
    To ensure we can send parameters to endpoints, this DefaultManipulator returns a default value for the parameter
"""


class DefaultManipulator(SwagManipulator):
    def __init__(self, parameter_name, parameter_type, default_value=None):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.default_value = default_value
        super().__init__(self.parameter_name, self.parameter_type, self.default_value)

    def generate(self):
        return self.default_value

    def get_rules(self):
        return "DEFAULT RULES"
