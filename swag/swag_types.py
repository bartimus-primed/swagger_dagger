"""
Swag types is broken off so there is an easier way to fuzz the parameters. We can do all the checks inside here as well as generate new outputs.
If someone wants to write special fuzz cases or anything, they can essentially add them as a function and as long as it returns the _described_type
the SwagManager and SwagEndpoints can just ask for a new value.
"""


class SwagTypes:
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
        """
        We will generate the _described_type from the Descriptions endpoint
        """
        self._described_type = None

    def generate_fuzz(self):
        # Create the fuzzy stuffing
        pass
