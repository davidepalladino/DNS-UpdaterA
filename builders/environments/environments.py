from abc import abstractmethod, ABC


class Environment(ABC):
    """
    Abstract base class representing an environment configuration.

    This class defines the interface for environment configurations,
    specifically for retrieving the DNS record name.  Concrete subclasses
    will provide specific implementations for different environment setups.
    """
    _record_name: str

    @abstractmethod
    def get_record_name(self):
        """
        Abstract method to retrieve the DNS record name.

        Returns:
            The DNS record name as a string.
        """
        pass


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

    def get_record_name(self) -> str:
        """
        Returns the name of the DNS record.

        Returns:
            The name of the DNS record.
        """
        return self._record_name

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