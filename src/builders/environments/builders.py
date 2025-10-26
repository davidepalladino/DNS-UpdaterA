import os

from abc import ABC, abstractmethod
from dotenv import load_dotenv

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
                self._record_name = self._get_arg(args, ARG_NAME)
            else:
                raise Exception("You must provide a record name to update.")
        except IndexError:
            raise Exception("You must provide a record name to update.")

    def _get_arg(self, args: list[str], arg: str) -> str:
        """
        Retrieves the value of a specific argument from a list of arguments. Checks if the argument
        is prefixed with "--" and raises an exception if it is. Returns the lowercased value of the
        specified argument.

        Parameters:
        args: list
            A list of arguments to process.
        arg: str
            The specific argument to locate and retrieve its associated value.

        Raises:
        Exception
            If the specified argument starts with "--".

        Returns:
        str
            The lowercased value associated with the specified argument.
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
        Sets authentication details by loading environment variables and arguments.

        This method attempts to retrieve the necessary authentication details for a
        Cloudflare integration using a combination of runtime arguments and environment
        variables. It prioritizes runtime arguments for the zone ID if provided.
        Otherwise, it falls back to predefined environmental variables. If any of the
        required details are missing, an exception is raised with information about the
        missing variables.

        Args:
            args: list
                A list of arguments to extract authentication details.

        Raises:
            EnvironmentError
                If any required variables (zone ID, email, or API key) are not set
                in the environment or runtime arguments.
        """
        load_dotenv()

        errors: list[str] = []
        zone_id: str | None = None

        if ARG_CLOUDFLARE_ZONE_ID in args:
            try:
                zone_id = self._get_arg(args, ARG_CLOUDFLARE_ZONE_ID)
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
        Sets the authentication for the application by loading required environment
        variables. This method validates the presence of mandatory environment variables
        and raises an exception if any of them are missing.

        Raises
        ------
        EnvironmentError
            Indicates that required environment variables are not set. A list of the
            missing variables is provided in the error message.

        Parameters
        ----------
        args : list
            A list of arguments. Note: This parameter is not utilized in the function
            but may be reserved for future use or required to match a specific method
            signature.
        """
        load_dotenv()

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
