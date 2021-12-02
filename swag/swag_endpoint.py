from swag.swag_types import SwagTypes


class SwagEndpoint:
    def __init__(self, location, raw_json):
        self.parameters = []
        self.location = location
        self.path_vars = self.location.split("/")
        self.details = raw_json
        self.parse_parameters()

    def parse_parameters(self):
        for p in self.path_vars:
            if p.__contains__("{") and p.__contains__("}"):
                self.parameters.append(p)
