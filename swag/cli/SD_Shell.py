import cmd
import os
from swag.swag_manager import SwagManager
from swag.cli.SD_Endpoint import SD_Endpoint
CLEAR_COMMAND = "cls"
if os.name != "nt":
    CLEAR_COMMAND = "clear"


class SD_Shell(cmd.Cmd):
    intro = "Swagger Dagger interactive shell"

    def __init__(self, endpoint):
        self.swagger_endpoint = endpoint
        self.swag_manager = SwagManager(self.swagger_endpoint)
        self.host_queried = False
        self.endpoints_queried = False
        self.endpoint_count = "Need to query the endpoint"
        self.target_endpoint = ""
        self.prompt = f"({self.swagger_endpoint}) "
        self.intro = self.get_intro()
        super().__init__(self)

    def get_intro(self):
        return f"Endpoint Count: {self.endpoint_count}\n"

    def cmdloop(self):
        return super().cmdloop(self.get_intro())

    def precmd(self, line: str) -> str:
        if line.__contains__("help") or line.__contains__("?"):
            self.emptyline()
        return super().precmd(line)

    def postcmd(self, stop: bool, line: str) -> bool:
        if not self.host_queried:
            print("You need to query the endpoint first")
            return
        return super().postcmd(stop, line)

    def preloop(self) -> None:
        os.system(CLEAR_COMMAND)
        return super().preloop()

    def postloop(self) -> None:
        return super().postloop()

    def do_query(self, args):
        """Connect to the host and get available endpoints"""
        answer = input(
            "You are about to connect to the endpoint... press y to continue. ")
        if not answer.__contains__("y"):
            self.emptyline()
            return
        self.swag_manager.get_swag_endpoint_data()
        self.endpoint_count = self.swag_manager.get_endpoint_count()
        self.host_queried = True
        self.emptyline()

    def do_quit(self, args):
        """Exit"""
        exit()

    def do_exit(self, args):
        """Exit"""
        exit()

    def do_list(self, args):
        """
        List the available endpoints
        - To List only OPEN endpoints:
        (host) list open

        """
        if not self.host_queried:
            return
        if not self.endpoints_queried:
            answer = input(
                f"You are about to check connectivity to {self.swag_manager.get_endpoint_count()} endpoints... press y to continue. ")
            if not answer.__contains__("y"):
                self.emptyline()
                return
            self.swag_manager.test_connections()
            self.endpoints_queried = True
        self.emptyline()
        if args.__contains__("open"):
            print("Open Endpoints:")
            self.swag_manager.list_endpoints(True)
            return
        self.swag_manager.list_endpoints()

    def do_select(self, args):
        """
        After listing the endpoints, select an endpoint to interact with
        select ENDPOINT_NUMBER
        """
        if not args:
            print("You kind of need to select something...")
            return
        ep_item = self.swag_manager.get_endpoint(int(args))
        if not ep_item:
            print("Invalid Endpoint number selected")
            return
        SD_Endpoint(ep_item)
        self.lastcmd = ""

    def emptyline(self) -> bool:
        os.system(CLEAR_COMMAND)
        print(self.get_intro())
