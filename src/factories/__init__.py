from typing import Union

from .providers.creators import CloudflareProviderCreator
from .providers.creators import OvhProviderCreator

ProviderCreator = Union[CloudflareProviderCreator, OvhProviderCreator]

__all__ = ["CloudflareProviderCreator", "OvhProviderCreator", "ProviderCreator"]
