import argparse
from swag.swag_manager import SwagManager


def main(swagger_endpoint):
    swag_api = SwagManager(swagger_endpoint)
    swag_api.test_connections()
    swag_api.detect_open_endpoints()
    # swag_api.print_open_endpoints(only_show_parameters=True)
    for e in swag_api.open_endpoints:
        print(e.endpoint_location)
    # for _e in swag_api.endpoints:
    #     for meth in swag_api.endpoints[_e].methods:
    #         for req_p in meth.required_parameters:
    #             for manipulator in req_p.manipulators:
    #                 if manipulator.default_value is not None:
    #                     print(manipulator)
    #         for opt_p in meth.optional_parameters:
    #             for manipulator in opt_p.manipulators:
    #                 if manipulator.default_value is not None:
    #                     print(manipulator)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Swagger Dagger will attempt to probe API endpoints based on Swagger's json endpoint. You might use swagger to help expose your API, but what do you use to check if your API exposes you?", usage="python main.py http://192.168.1.1/v2/{swagger's json endpoint}")
    argparser.add_argument("SwaggerEndpoint",
                           help="Point me to the swagger json endpoint")
    # argparser.add_argument(
    #     "-Endpoint", help="If you don't know where the json endpoint is, just give the web address and try to bruteforce it", required=False)
    args = argparser.parse_args()
    main(args.SwaggerEndpoint)
