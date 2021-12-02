import argparse
from swag.swag_manager import SwagManager


def main(swagger_endpoint):
    swag_api = SwagManager(swagger_endpoint)
    for ep, ep_data in swag_api.endpoints.items():
        for method in ep_data.methods:
            method.test_connection()

    # print(swag_api.definitions.keys())


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("SwaggerEndpoint",
                           help="Point me to the swagger json endpoint")
    args = argparser.parse_args()
    main(args.SwaggerEndpoint)
