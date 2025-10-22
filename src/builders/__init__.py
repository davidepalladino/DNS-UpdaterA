from typing import Union

from .environments.director import EnvironmentDirector
from .environments.models import CloudflareEnvironmentModel, OvhEnvironmentModel

EnvironmentModel = Union[CloudflareEnvironmentModel, OvhEnvironmentModel]

__all__ = ["EnvironmentDirector", "EnvironmentModel"]
