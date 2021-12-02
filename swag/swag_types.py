import json
"""
Swag types is broken off so there is an easier way to fuzz the parameters. We can do all the checks inside here as well as generate new outputs.
If someone wants to write special fuzz cases or anything, they can essentially add them as a class and add that to a swag_endpoint's methods list
"""


class SwagTypes:
    def __init__(self, parameter_name, parameter_type):
        self.parameter_name = parameter_name
        """
        TODO: We will generate the _described_type from the Descriptions endpoint
        """
        self._described_type = parameter_type

    def generate_fuzz(self):
        # Create the fuzzy stuffing
        pass


class SE_GET:
    def __init__(self, raw_json):
        self.send_type = None
        self.parameters = None
        self.receive_type = None
        self.summary = None
        self.responses = []
        self.build_data(raw_json)

    def build_data(self, details):
        for k, v in details.items():
            match(k):
                case "consumes":
                    self.send_type = v
                case "parameters":
                    self.parameters = v
                case "produces":
                    self.receive_type = v
                case "summary":
                    self.summary = v
                case "responses":
                    for sub_k, sub_v in v.items():
                        if sub_v["description"] is not None:
                            self.responses.append(SE_RESPONSE(
                                sub_k, sub_v["description"]))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()


class SE_POST:
    def __init__(self, raw_json):
        self.send_type = None
        self.parameters = None
        self.receive_type = None
        self.summary = None
        self.responses = []
        self.build_data(raw_json)

    def build_data(self, details):
        for k, v in details.items():
            match(k):
                case "consumes":
                    self.send_type = v
                case "parameters":
                    self.parameters = v
                case "produces":
                    self.receive_type = v
                case "summary":
                    self.summary = v
                case "responses":
                    for sub_k, sub_v in v.items():
                        if sub_v["description"] is not None:
                            self.responses.append(SE_RESPONSE(
                                sub_k, sub_v["description"]))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()


class SE_RESPONSE:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJson()
