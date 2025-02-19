import os

from abc import ABC, abstractmethod
from dotenv import load_dotenv

from builders.environments.environments import CloudflareEnvironment, Environment, OvhEnvironment
from consts.arguments import ARG_NAME
from consts.environments import ENV_CLOUDFLARE_ZONE_ID, ENV_CLOUDFLARE_EMAIL, ENV_CLOUDFLARE_API_KEY, ENV_OVH_ENDPOINT, \
    ENV_OVH_APPLICATION_KEY, ENV_OVH_APPLICATION_SECRET, ENV_OVH_CONSUMER_KEY


class EnvironmentBuilder(ABC):
    """
    Abstract base class for building environment configurations.  Defines the
    interface for setting the record name and authentication details.
    """

    _record_name: str

    def set_record_name(self, args: list):
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
                self._record_name = args[args.index(ARG_NAME) + 1].lower()
                if self._record_name.startswith("--"):
                    raise Exception(f"'{self._record_name}' is not allowed for '{ARG_NAME}' argument.")
            else:
                raise Exception("You must provide a record name to update.")
        except IndexError:
            raise Exception("You must provide a record name to update.")

    @abstractmethod
    def set_authentication(self):
        """
        Sets the authentication details from environment variables.

        Returns:
            The builder instance (self) to allow method chaining.

        Raises:
            EnvironmentError: If required environment variables are not set.
        """
        pass

    @abstractmethod
    def make(self) -> Environment:  # Changed to return Environment
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

    _record_name = None
    _zone_id = None
    _email = None
    _api_key = None

    def set_authentication(self):
        """
        Sets the authentication details from environment variables.

        Returns:
            The builder instance (self) to allow method chaining.

        Raises:
            EnvironmentError: If required environment variables are not set.
        """
        load_dotenv()

        errors: list = []

        self._zone_id = os.getenv(ENV_CLOUDFLARE_ZONE_ID)
        if self._zone_id is None:
            errors.append(ENV_CLOUDFLARE_ZONE_ID)

        self._email = os.getenv(ENV_CLOUDFLARE_EMAIL)
        if self._email is None:
            errors.append(ENV_CLOUDFLARE_EMAIL)

        self._api_key = os.getenv(ENV_CLOUDFLARE_API_KEY)
        if self._api_key is None:
            errors.append(ENV_CLOUDFLARE_API_KEY)

        if len(errors) > 0:
            raise EnvironmentError(f"Please set environment for: {', '.join(errors)}.")

    def make(self) -> CloudflareEnvironment:
        """
        Creates and returns a CloudflareEnvironment instance.

        Returns:
            A CloudflareEnvironment instance.
        """
        return CloudflareEnvironment(self._record_name, self._zone_id, self._email, self._api_key)


class OvhEnvironmentBuilder(EnvironmentBuilder):
    """
    Concrete implementation of EnvironmentBuilder for creating
    OvhEnvironment instances.
    """

    _endpoint: str
    _application_key: str
    _application_secret: str
    _consumer_key: str

    def set_authentication(self):
        """
        Sets the authentication details from environment variables.

        Returns:
            The builder instance (self) for method chaining.

        Raises:
            EnvironmentError: If required environment variables are not set.
        """
        load_dotenv()

        errors: list = []

        self._endpoint = os.getenv(ENV_OVH_ENDPOINT)
        if self._endpoint is None:
            errors.append(ENV_OVH_ENDPOINT)

        self._application_key = os.getenv(ENV_OVH_APPLICATION_KEY)
        if self._application_key is None:
            errors.append(ENV_OVH_APPLICATION_KEY)

        self._application_secret = os.getenv(ENV_OVH_APPLICATION_SECRET)
        if self._application_secret is None:
            errors.append(ENV_OVH_APPLICATION_SECRET)

        self._consumer_key = os.getenv(ENV_OVH_CONSUMER_KEY)
        if self._consumer_key is None:
            errors.append(ENV_OVH_CONSUMER_KEY)

        if len(errors) > 0:
            raise EnvironmentError(f"Please set environment for: {', '.join(errors)}.")

    def make(self) -> OvhEnvironment:
        """
         Creates and returns an OvhEnvironment instance.

         Returns:
             An OvhEnvironment instance.
         """
        return OvhEnvironment(self._record_name, self._endpoint, self._application_key, self._application_secret, self._consumer_key)