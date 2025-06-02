from builders.environments.builders import CloudflareEnvironmentBuilder, OvhEnvironmentBuilder
from builders.environments.environments import CloudflareEnvironment, OvhEnvironment


class EnvironmentDirector:
    """
    Directs the construction of specific Environment objects using builders.

    This class decouples the creation of Environment objects from their
    representation, allowing for different configurations to be built.
    """

    def make_cloudflare_environment(self, args: list) -> CloudflareEnvironment:
        """
        Constructs a CloudflareEnvironment object.

        Args:
            args: A list of command-line arguments to configure the environment.

        Returns:
            A CloudflareEnvironment instance.

        Raises:
            ValueError: If there's an issue with the record name argument.
            EnvironmentError: If required environment variables are not set.
        """
        builder = CloudflareEnvironmentBuilder()
        builder.set_record_name(args)
        builder.set_authentication(args)
        return builder.make()

    def make_ovh_environment(self, args: list) -> OvhEnvironment:
        """
        Constructs an OvhEnvironment object.

        Args:
            args: A list of command-line arguments (potentially used for record name).

        Returns:
            An OvhEnvironment instance.

        Raises:
            EnvironmentError: If required environment variables are not set.
        """
        builder = OvhEnvironmentBuilder()
        builder.set_record_name(args)
        builder.set_authentication(args)
        return builder.make()