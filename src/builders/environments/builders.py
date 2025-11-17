import os

from abc import ABC, abstractmethod
from dotenv import dotenv_values

from .models import EnvironmentModel, CloudflareEnvironmentModel, OvhEnvironmentModel
from src.consts import (
    ARG_CLOUDFLARE_ZONE_ID,
    ARG_NAME,
    ENV_CLOUDFLARE_ZONE_ID,
    ENV_CLOUDFLARE_EMAIL,
    ENV_CLOUDFLARE_API_KEY,
    ENV_OVH_ENDPOINT,
    ENV_OVH_APPLICATION_KEY,
    ENV_OVH_APPLICATION_SECRET,
    ENV_OVH_CONSUMER_KEY,
)


class EnvironmentBuilder(ABC):
    """
    Abstract base class for building environment configurations.  Defines the
    interface for setting the record name and authentication details.
    """

    _record_name: str

    def set_record_name(self, args: list[str]) -> None:
        """
        Sets the record name from command-line arguments.

        Args:
            args: A list of command-line arguments.

        Returns:
            The builder instance (self) to allow method chaining.

        Raises:
            ValueError: If the record name argument is missing or invalid.
        """
        try:
            if ARG_NAME in args:
                self._record_name = self._get_program_arg(args, ARG_NAME)
            else:
                raise Exception("You must provide a record name to update.")
        except IndexError:
            raise Exception("You must provide a record name to update.")

    def _load_environments(self) -> None:
        """
        Loads environment variables from a .env file and sets them in the system environment.

        Summary:
        This method retrieves key-value pairs from a .env file using `dotenv_values`,
        and sets them in the environment variables of the system only if they are not
        already set.

        Raises:
            None

        Returns:
            None
        """
        for key, value in dotenv_values().items():
            os.environ.setdefault(key, value)

    def _get_program_arg(self, args: list[str], arg: str) -> str:
        """
        Retrieves the value of a specified program argument from the provided list of arguments.

        The function searches for the specified argument in the list and retrieves its corresponding value.
        The value is converted to lowercase before being returned. An exception is raised if the detected
        value starts with '--', as such a string is considered invalid for the specified argument.

        Parameters:
            args (list[str]): List of command-line argument strings.
            arg (str): The argument whose associated value should be retrieved.

        Returns:
            str: The value associated with the specified argument in the list.

        Raises:
            Exception: If the retrieved value starts with '--', indicating an invalid format.
        """
        value: str = args[args.index(arg) + 1].lower()
        if value.startswith("--"):
            raise Exception(f"'{value}' is not allowed for '{arg}' argument.")
        return value

    @abstractmethod
    def set_authentication(self, args: list[str]) -> None:
        """
        Defines an abstract method for setting authentication, which should be
        implemented by any concrete subclass. This method is responsible for
        configuring the necessary authentication mechanism based on the input
        parameters.

        Args:
            args (list): A list containing authentication-related parameters
            required for setting up the authentication mechanism.

        Returns:
            None
        """
        pass

    @abstractmethod
    def make(self) -> EnvironmentModel:  # Changed to return Environment
        """
        Creates and returns an Environment instance.

        Returns:
            An Environment instance.
        """
        pass


class CloudflareEnvironmentBuilder(EnvironmentBuilder):
    """
    Concrete implementation of EnvironmentBuilder for creating
    CloudflareEnvironment instances.
    """

    _record_name: str
    _zone_id: str
    _email: str
    _api_key: str

    def set_authentication(self, args: list[str]) -> None:
        """
        Sets authentication details required for accessing Cloudflare API by
        loading environment variables or processing command-line arguments.

        This method first loads the environment variables. Then, it attempts
        to retrieve the necessary Cloudflare credentials (Zone ID, Email, and
        API key) either from the provided command-line arguments or
        environment variables. If any required credential is missing, an
        appropriate error is raised.

        Args:
            args: A list of command-line arguments to check for specific
                  credentials.

        Raises:
            Exception: If the provided arguments do not include a valid
                       Cloudflare Zone ID when expected.
            EnvironmentError: If one or more required environment variables
                              are not set.
        """
        self._load_environments()

        errors: list[str] = []
        zone_id: str | None = None

        if ARG_CLOUDFLARE_ZONE_ID in args:
            try:
                zone_id = self._get_program_arg(args, ARG_CLOUDFLARE_ZONE_ID)
            except IndexError:
                raise Exception("You must provide a valid Cloudflare Zone ID.")
        else:
            zone_id = os.getenv(ENV_CLOUDFLARE_ZONE_ID)

        if zone_id is None:
            errors.append(ENV_CLOUDFLARE_ZONE_ID)
        else:
            self._zone_id = zone_id

        email = os.getenv(ENV_CLOUDFLARE_EMAIL)
        if email is None:
            errors.append(ENV_CLOUDFLARE_EMAIL)
        else:
            self._email = email

        api_key = os.getenv(ENV_CLOUDFLARE_API_KEY)
        if api_key is None:
            errors.append(ENV_CLOUDFLARE_API_KEY)
        else:
            self._api_key = api_key

        if len(errors) > 0:
            raise EnvironmentError(f"Please set environment for: {', '.join(errors)}.")

    def make(self) -> CloudflareEnvironmentModel:
        """
        Creates and returns a CloudflareEnvironment instance.

        Returns:
            A CloudflareEnvironment instance.
        """
        return CloudflareEnvironmentModel(
            self._record_name, self._zone_id, self._email, self._api_key
        )


class OvhEnvironmentBuilder(EnvironmentBuilder):
    """
    Concrete implementation of EnvironmentBuilder for creating
    OvhEnvironment instances.
    """

    _endpoint: str
    _application_key: str
    _application_secret: str
    _consumer_key: str

    def set_authentication(self, args: list[str]) -> None:
        """
        Sets up authentication parameters by loading environment variables required for OVH API interaction.

        This method attempts to load necessary credentials from environment variables. If any of the required
        variables are missing, it raises an exception to notify the user.

        Parameters:
            args (list[str]): Additional arguments to process, currently unused.

        Raises:
            EnvironmentError: Raised if any required environment variables are not set.
        """
        self._load_environments()

        errors: list[str] = []

        endpoint = os.getenv(ENV_OVH_ENDPOINT)
        if endpoint is None:
            errors.append(ENV_OVH_ENDPOINT)
        else:
            self._endpoint = endpoint

        application_key = os.getenv(ENV_OVH_APPLICATION_KEY)
        if application_key is None:
            errors.append(ENV_OVH_APPLICATION_KEY)
        else:
            self._application_key = application_key

        application_secret = os.getenv(ENV_OVH_APPLICATION_SECRET)
        if application_secret is None:
            errors.append(ENV_OVH_APPLICATION_SECRET)
        else:
            self._application_secret = application_secret

        consumer_key = os.getenv(ENV_OVH_CONSUMER_KEY)
        if consumer_key is None:
            errors.append(ENV_OVH_CONSUMER_KEY)
        else:
            self._consumer_key = consumer_key

        if len(errors) > 0:
            raise EnvironmentError(f"Please set environment for: {', '.join(errors)}.")

    def make(self) -> OvhEnvironmentModel:
        """
        Creates and returns an OvhEnvironment instance.

        Returns:
            An OvhEnvironment instance.
        """
        return OvhEnvironmentModel(
            self._record_name,
            self._endpoint,
            self._application_key,
            self._application_secret,
            self._consumer_key,
        )
