import cmd
import os
from swag.cli.SD_Parameter import SD_Parameter
CLEAR_COMMAND = "cls"
if os.name != "nt":
    CLEAR_COMMAND = "clear"


class SD_Method(cmd.Cmd):
    intro = "Interact with a Endpoint's Method"

    def __init__(self, method_item):
        self.method = method_item.method
        self.method_item = method_item
        self.prompt = f"({self.method} {self.method_item.endpoint_location}) "
        self.intro = self.get_intro()
        super().__init__()
        os.system(CLEAR_COMMAND)
        super().cmdloop(self.get_intro())

    def get_intro(self):
        final_out = f"Interacting with Method: {self.method} {self.method_item.endpoint_location}\n"
        for idx, parameter in enumerate(self.method_item.all_parameters):
            final_out += f"{idx}. Method Parameter: {parameter.name}\n\tType: {parameter.type_of}\n\tRequired: {parameter.required}\n\tDefault: {parameter.default}\n"
        return final_out

    def do_select(self, args):
        """
        Select a Parameter to interact with it.
        """
        parameter_item = self.method_item.get_parameter(int(args))
        if not parameter_item:
            print("Invalid parameter selected")
            return
        SD_Parameter(parameter_item,
                     f"{self.method} {self.method_item.endpoint_location}")
        self.lastcmd = ""

    def do_fuzz(self, args):
        answer = input(
            f"You are about to fuzz {self.method_item.endpoint_location}, this is considered malicious... press y to continue. ")
        if not answer.__contains__("y"):
            self.emptyline()
            return
        self.method_item.test_endpoint_connection(True, True)

    def do_connect(self, args):
        answer = input(
            f"You are about to check connectivity to {self.method_item.endpoint_location}... press y to continue. ")
        if not answer.__contains__("y"):
            self.emptyline()
            return
        self.method_item.test_endpoint_connection(True)

    def do_quit(self, args):
        """Exit"""
        return True

    def do_exit(self, args):
        """Exit"""
        return True

    def emptyline(self) -> bool:
        os.system(CLEAR_COMMAND)
        print(self.get_intro())
