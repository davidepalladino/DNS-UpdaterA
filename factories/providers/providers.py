from __future__ import annotations

import http.client
import json

from abc import ABC, abstractmethod
from typing import Union
from factories.providers.dtos import RecordDTO


class Provider(ABC):
    """
    Abstract base class for DNS provider implementations.  Defines the
    interface for interacting with a DNS service.
    """

    @abstractmethod
    def get(self, name: str) -> Union[RecordDTO, None]:
        """
        Retrieves a DNS record by name.

        Args:
            name: The name of the DNS record to retrieve.

        Returns:
            A RecordDTO object representing the DNS record if found,
            otherwise None.
        """
        pass

    @abstractmethod
    def update(self, record: RecordDTO, ip: str) -> list[str]:
        """
        Updates a DNS record with a new IP address.

        Args:
            record: The DNS record to update.
            ip: The new IP address to set for the DNS record.

        Returns:
            A list of error messages (strings), if any occurred during the
            update.  Returns an empty list if the update was successful.
        """
        pass

class CloudflareProvider(Provider):
    """
    A concrete implementation of the Provider interface for interacting
    with the Cloudflare DNS API.
    """

    _connection = http.client.HTTPSConnection("api.cloudflare.com")
    _zone_id: str
    _headers: dict

    def __init__(self, zone_id: str, email: str, api_key: str):
        """
        Initializes a CloudflareProvider instance.

        Args:
            zone_id: The Cloudflare zone ID.
            email: The Cloudflare account email.
            api_key: The Cloudflare API key.
        """
        self._zone_id = zone_id
        self._headers = {
            'Content-Type': "application/json",
            'X-Auth-Email': email,
            'X-Auth-Key': api_key
        }

    def get(self, name: str) -> Union[RecordDTO, None]:
        """
        Retrieves a DNS record by name from the Cloudflare zone.

        Args:
            name: The name of the DNS record to retrieve.

        Returns:
            A RecordDTO object representing the DNS record if found,
            otherwise None.
        """

        self._connection.request(
            method="GET",
            url=f"/client/v4/zones/{self._zone_id}/dns_records?type=A&name={name}",
            headers=self._headers
        )
        result = self._connection.getresponse()
        data = json.loads(result.read().decode("utf-8"))

        try:
            return RecordDTO(data['result'][0]['id'], data['result'][0]['name'], data['result'][0]['content'])
        except IndexError:
            return None

    def update(self, record: RecordDTO, ip: str) -> list[str]:
        """
        Updates a DNS record with a new IP address in the Cloudflare zone.

        Args:
            record: The DNS record to update.
            ip: The new IP address to set for the DNS record.

        Returns:
            A list of error messages (strings), if any occurred during the
            update.  Returns an empty list if the update was successful.
        """
        body = "{\n \"content\": \"" + ip + "\" \n}"
        self._connection.request(
            method="PATCH",
            url=f"/client/v4/zones/{self._zone_id}/dns_records/{record.get_id()}",
            body=body,
            headers=self._headers
        )

        result = self._connection.getresponse()
        data = json.loads(result.read().decode("utf-8"))

        return data['errors']