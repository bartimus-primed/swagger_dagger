from swag.swag_manipulator import SwagManipulator


class IntegerManipulator(SwagManipulator):
    def __init__(self, parameter_name, parameter_type, parameter_location, default_value=None):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.default_value = default_value
        self.parameter_location = parameter_location
        super().__init__(self.parameter_name, self.parameter_type,
                         self.parameter_location, self.default_value)
        self.generate()

    def generate(self):
        if self.default_value:
            self.add_to_queue(self.default_value)
        else:
            self.add_to_queue(self.get_rules())

    def permutate(self, original_value):
        return self.get_rules()

    def get_rules(self):
        return "INTEGERRULE"
