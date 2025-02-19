import os
import sys

from logging.handlers import TimedRotatingFileHandler

from builders.environments.director import EnvironmentDirector
from consts.arguments import ARG_PROVIDER
from factories.providers.creators import CloudflareProviderCreator, OvhProviderCreator
from utils.logger import *


def set_logger():
    """
    Sets up the logging configuration.

    Creates a log directory if it doesn't exist and configures a timed rotating
    file handler to log messages to a file named 'main' in the logs directory.
    """
    exec_path = sys.argv[0].removesuffix("/main.py")

    log_path = f"{exec_path}/logs"
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s: %(message)s",
        level=logging.INFO,
        handlers=[
            TimedRotatingFileHandler(
                filename=f"{exec_path}/logs/main",
                when="midnight",
                interval=1,
                backupCount=15
            )
        ]
    )

def get_provider(args: list) -> str:
    """
    Gets the provider name from command-line arguments.

    Args:
        args: A list of command-line arguments.

    Returns:
        The provider name as a string.

    Raises:
        ValueError: If the provider argument is missing or invalid.
    """
    try:
        if ARG_PROVIDER in args:
            provider = args[args.index(ARG_PROVIDER) + 1].lower()
            if provider.startswith("--"):
                raise Exception(f"'{provider}' is not allowed for '{ARG_PROVIDER}' argument.")
            return provider
        else:
            raise Exception("You must provide a provider to update.")
    except IndexError:
        raise Exception("You must provide a provider to update.")


if __name__ == '__main__':
    args = sys.argv[1:]

    set_logger()

    try:
        provider = get_provider(args)

        director = EnvironmentDirector()

        environment = None
        creator = None

        if provider == "cloudflare":
            environment = director.make_cloudflare_environment(args)
            creator = CloudflareProviderCreator(environment.get_zone_id(), environment.get_email(), environment.get_api_key())
        elif provider == "ovh":
            environment = director.make_ovh_environment(args)
            creator = OvhProviderCreator(environment.get_endpoint(), environment.get_application_key(), environment.get_application_secret(), environment.get_consumer_key())
        else:
            raise Exception(f"You must provide a valid provider to update, or {provider} is not covered yet.")

        update_result = creator.updateIfChanged(environment.get_record_name())
        Logger.info(update_result.get_reason())

    except Exception as error:
        Logger.error(error.__str__())
        exit(1)