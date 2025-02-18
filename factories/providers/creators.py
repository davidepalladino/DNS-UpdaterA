from __future__ import annotations

from abc import ABC, abstractmethod

from factories.providers.dtos import ResultUpdateDTO
from factories.providers.providers import Provider, CloudflareProvider
from requests import get


class ProviderCreator(ABC):
    """
    Abstract base class for creating DNS provider instances. Provides a
    template for creating and updating DNS records.
    """

    @abstractmethod
    def _make(self) :
        """
        Abstract factory method to create a specific Provider instance.

        Returns:
            A Provider instance.
        """
        pass

    def updateIfChanged(self, name) -> ResultUpdateDTO:
        """
        Updates a DNS record if the public IP address has changed.

        Retrieves the current DNS record, gets the current public IP address,
        and updates the record if the IP addresses are different.

        Args:
            name: The name of the DNS record to update.

        Returns:
            A ResultUpdateDTO object indicating the result of the update
            operation.

        Raises:
            Exception: If the DNS record is not found or if the update fails.
        """
        provider = self._make()

        record = provider.get(name)
        if record is None:
            raise Exception(f"Record '{name}' not found.")

        public_ip = self._get_public_ip()
        if record.get_ip() != public_ip:
            errors: list[str] = provider.update(record.get_id(), public_ip)
            if len(errors) != 0:
                raise Exception(f"Record update failed with these reasons: {errors}.")
            return ResultUpdateDTO(True, f"Record update successful for '{name}'.")

        return ResultUpdateDTO(False, f"Record not updated for '{name}' because hasn't changed.")

    def _get_public_ip(self) -> str:
        """
        Retrieves the current public IP address.

        Returns:
            The current public IP address as a string.

        Raises:
            requests.exceptions.RequestException: If there's an issue with the
              request to the ipify service.
        """
        return get('https://api.ipify.org').content.decode('utf8')


class CloudflareProviderCreator(ProviderCreator):
    """
    A concrete implementation of ProviderCreator for creating
    CloudflareProvider instances.
    """

    _zone_id: str
    _email: str
    _api_key: str

    def __init__(self, zone_id: str, email: str, api_key: str):
        """
        Initializes a CloudflareProviderCreator instance.

        Args:
            zone_id: The Cloudflare zone ID.
            email: The Cloudflare account email.
            api_key: The Cloudflare API key.
        """
        self._zone_id = zone_id
        self._email = email
        self._api_key = api_key

    def _make(self) -> Provider:
        return CloudflareProvider(self._zone_id, self._email, self._api_key)