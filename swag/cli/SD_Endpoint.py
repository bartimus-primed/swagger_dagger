import cmd
import os
from swag.cli.SD_Method import SD_Method
CLEAR_COMMAND = "cls"
if os.name != "nt":
    CLEAR_COMMAND = "clear"


class SD_Endpoint(cmd.Cmd):
    intro = "Interact with a specific Host Endpoint"

    def __init__(self, endpoint_item):
        self.endpoint = endpoint_item.endpoint_location
        self.swag_endpoint = endpoint_item
        self.prompt = f"({self.endpoint}) "
        self.intro = self.get_intro()
        super().__init__()
        super().cmdloop(self.get_intro())

    def get_intro(self):
        final_out = f"Interacting with: {self.endpoint}\n"
        methods = self.swag_endpoint.list_methods()
        for k, v in methods.items():
            other_string = f"Supported Method: {k}\n"
            for param in v:
                other_string += f"\tParameter Name: {param}\n"
            final_out += other_string
        return final_out

    def do_quit(self, args):
        """Exit"""
        return True

    def do_exit(self, args):
        """Exit"""
        return True

    def do_select(self, args):
        """
        Select a method to interact with it.
        """
        method_item = self.swag_endpoint.get_method(args.upper())
        if not method_item:
            print("Invalid method selected")
            return
        SD_Method(method_item)
        self.lastcmd = ""

    def emptyline(self) -> bool:
        os.system(CLEAR_COMMAND)
        print(self.get_intro())
