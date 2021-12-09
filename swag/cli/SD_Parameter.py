import cmd
import os
CLEAR_COMMAND = "cls"
if os.name != "nt":
    CLEAR_COMMAND = "clear"


class SD_Parameter(cmd.Cmd):
    intro = "Interact with a Method's Parameter"

    def __init__(self, parameter_item, endpoint_name):
        self.endpoint_name = endpoint_name
        self.parameter = parameter_item.name
        self.parameter_item = parameter_item
        self.prompt = f"({self.parameter} {self.endpoint_name}) "
        self.intro = self.get_intro()
        super().__init__()
        os.system(CLEAR_COMMAND)
        super().cmdloop(self.get_intro())

    def get_intro(self):
        return f"Interacting with Parameter: {self.parameter} {self.endpoint_name}\n{self.parameter_item.describe()}"

    def do_quit(self, args):
        """Exit"""
        return True

    def do_exit(self, args):
        """Exit"""
        return True

    def emptyline(self) -> bool:
        os.system(CLEAR_COMMAND)
        print(self.get_intro())
