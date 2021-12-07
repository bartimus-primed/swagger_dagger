import argparse
from swag.swag_manager import SwagManager


def main(swagger_endpoint):
    swag_api = SwagManager(swagger_endpoint)
    swag_api.test_connections()
    swag_api.detect_open_endpoints()
    for _e in swag_api.endpoints:
        for meth in swag_api.endpoints[_e].methods:
            if meth.all_parameters:
                meth.generate_parameter_url()
            if meth.fuzzed_endpoint_location is not None:
                meth.test_fuzzed_endpoint_connection(print_response=True)
                if meth.successful_response:
                    print(meth.successful_response)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Swagger Dagger will attempt to probe API endpoints based on Swagger's json endpoint. You might use swagger to help expose your API, but what do you use to check if your API exposes you?", usage="python main.py http://192.168.1.1/v2/{swagger's json endpoint}")
    argparser.add_argument("SwaggerEndpoint",
                           help="Point me to the swagger json endpoint")
    # argparser.add_argument(
    #     "-Endpoint", help="If you don't know where the json endpoint is, just give the web address and try to bruteforce it", required=False)
    args = argparser.parse_args()
    main(args.SwaggerEndpoint)
