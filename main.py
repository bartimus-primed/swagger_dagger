import argparse
from swag.swag_manager import SwagManager


def main(swagger_endpoint):
    swag_api = SwagManager(swagger_endpoint)
    swag_api.test_connections()
    swag_api.check_successful()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("SwaggerEndpoint",
                           help="Point me to the swagger json endpoint")
    args = argparser.parse_args()
    main(args.SwaggerEndpoint)
