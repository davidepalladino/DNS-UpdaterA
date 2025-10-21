from abc import ABC


class Environment(ABC):
    """
    Abstract base class representing an environment configuration.

    This class defines the interface for environment configurations,
    specifically for retrieving the DNS record name.  Concrete subclasses
    will provide specific implementations for different environment setups.
    """
    _record_name: str

    def get_record_name(self) -> str:
        """
        Returns the name of the DNS record.

        Returns:
            The name of the DNS record.
        """
        return self._record_name


class CloudflareEnvironment(Environment):
    """
    Represents the environment configuration for interacting with Cloudflare.

    This class stores the necessary information (record name, zone ID, email, and API key)
    required to connect to and update DNS records in a Cloudflare zone.  It inherits
    from the base `Environment` class.
    """

    _zone_id: str
    _email: str
    _api_key: str

    def __init__(self, record_name: str, zone_id: str, email: str, api_key: str):
        """
        Initializes a CloudflareEnvironment instance.

        Args:
            record_name: The name of the DNS record to manage.
            zone_id: The Cloudflare zone ID.
            email: The Cloudflare account email.
            api_key: The Cloudflare API key.
        """
        self._record_name = record_name
        self._zone_id = zone_id
        self._email = email
        self._api_key = api_key

    def get_zone_id(self) -> str:
        """
        Returns the Cloudflare zone ID.

        Returns:
            The Cloudflare zone ID.
        """
        return self._zone_id

    def get_email(self) -> str:
        """
        Returns the Cloudflare account email.

        Returns:
            The Cloudflare account email.
        """
        return self._email

    def get_api_key(self) -> str:
        """
        Returns the Cloudflare API key.

        Returns:
            The Cloudflare API key.
        """
        return self._api_key


class OvhEnvironment(Environment):
    """
    Represents the environment configuration for interacting with the OVH API.

    This class stores the necessary information (record name, endpoint,
    application key, application secret, and consumer key) required to
    connect to and update DNS records in an OVH zone. It inherits from
    the base `Environment` class.
    """

    _endpoint: str
    _application_key: str
    _application_secret: str
    _consumer_key: str

    def __init__(self, record_name: str, endpoint: str, application_key: str, application_secret: str, consumer_key: str):
        """
        Initializes an OvhEnvironment instance.

        Args:
            record_name: The name of the DNS record to manage.
            endpoint: The OVH API endpoint.
            application_key: The OVH application key.
            application_secret: The OVH application secret.
            consumer_key: The OVH consumer key.
        """
        self._record_name = record_name
        self._endpoint = endpoint
        self._application_key = application_key
        self._application_secret = application_secret
        self._consumer_key = consumer_key

    def get_endpoint(self) -> str:
        """
        Returns the OVH API endpoint.

        Returns:
            The OVH API endpoint.
        """
        return self._endpoint

    def get_application_key(self) -> str:
        """
        Returns the OVH application key.

        Returns:
            The OVH application key.
        """
        return self._application_key

    def get_application_secret(self) -> str:
        """
        Returns the OVH application secret.

        Returns:
            The OVH application secret.
        """
        return self._application_secret

    def get_consumer_key(self) -> str:
        """
        Returns the OVH consumer key.

        Returns:
            The OVH consumer key.
        """
        return self._consumer_key