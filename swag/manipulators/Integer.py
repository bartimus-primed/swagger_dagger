from swag.swag_manipulator import SwagManipulator


class IntegerManipulator(SwagManipulator):
    def __init__(self, parameter_name, parameter_type, default_value=None):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.default_value = default_value
        super().__init__(self.parameter_name, self.parameter_type, self.default_value)

    def generate(self):
        return self.get_rules()

    def get_rules(self):
        return "INTEGER RULES"
