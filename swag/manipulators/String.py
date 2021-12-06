from swag.swag_manipulator import SwagManipulator


class StringManipulator(SwagManipulator):
    def __init__(self, parameter_name, parameter_type, default_value):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.default_value = default_value
        super().__init__(self.parameter_name, self.parameter_type, self.default_value)

    def generate(self):
        if self.default_value:
            print(self.default_value)
        return self.get_rules()

    def get_rules(self):
        return "STRINGRULE"
