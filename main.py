import argparse
from swag.cli.SD_Shell import SD_Shell


def main(swagger_endpoint):
    SD_Shell(swagger_endpoint).cmdloop()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Swagger Dagger will attempt to probe API endpoints based on Swagger's json endpoint. You might use swagger to help expose your API, but what do you use to check if your API exposes you?",
        usage="python main.py http://192.168.1.1/v2/{swagger's json endpoint}")
    argparser.add_argument(
        "SwaggerEndpoint", help="Point me to the swagger json endpoint")

    args = argparser.parse_args()
    main(args.SwaggerEndpoint)
