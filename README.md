# DNS-UpdaterA
This script provides a framework for managing DNS records across different providers. It's designed:  
- to be a lightweight solution.  
- with a modular architecture that allows you to easily add support for new DNS providers.  

The current implementation includes support for OVH and Cloudflare.

## Features
- **Provider-Agnostic Design:** The core logic for fetching the public IP and updating DNS records is abstracted, allowing easy integration with various DNS providers.  
- **Pluggable Providers:** New DNS providers can be added by implementing a simple interface, without modifying the core logic, using the Factory Method pattern.  
- **Robust Error Handling:** Comprehensive error handling for API requests, environment variables, and argument parsing.  
- **Detailed Logging:** Logging with daily rotation and backups.  
- **Well-Documented Code:** Docstrings for all classes and functions.  
- **Builder Pattern:** Uses the Builder pattern for flexible environment configuration.
- **Docker Support:** Docker Compose file for easy deployment.

## Installation
### Standalone
#### Requirements
- [UV](https://docs.astral.sh/uv/getting-started/installation/).
- Makefile (only for Linux and MacOS).
- Dependencies are managed via `pyproject.toml`.

#### Steps
1. Clone or download this repository.  
2. Install the required dependencies using `uv`:
   2.1. If you are using Linux or MacOS: 
        ```bash
        make install
        make sync
        ```
        Instead, for a clean installation:
        ```bash
        make install-clean
        make sync
        ```
   2.2. If you are using Windows (please, change OS):
        ```bash
        uv venv --allow-existing
       	uv sync
        ```
        Instead, for a clean installation:
        ```bash
        uv venv -c
       	uv sync
        ```        
3. Create a `.env` file in the script directory with the required environment variables as described in the Configuration section.

#### Usage
Run the script, specifying the provider and record name:
```bash
uv run main.py --provider <provider> --name <record_name> [--zone-id <cloudflare_zone_id>]
```

### Docker
#### Requirements
- [Docker and Docker Compose](https://docs.docker.com/get-started/).

#### Steps
1. Clone or download this repository.
2. Create a `.env` file in the script directory with the required environment variables as described in the Configuration section.
3. Crate your cron file(s) (see `crontab.example`) under `cron` folder.
4. Build by using Docker Compose:
   ```bash
   docker compose up -d
   ```
#### `docker-compose.yml`
Into `docker-compose.yml` you can bind the `logs` folder to a specific host folder. The default is `./logs`.
Also, you can set the environment variables in the `environment` section. These variables take precedence over the `.env` file.

## Configuration
The configuration process depends on the chosen DNS provider. The script uses environment variables (under `.env` file) for authentication and other provider-specific settings.

### Cloudflare Configuration
```env
CLOUDFLARE_ZONE_ID=your_zone_id
CLOUDFLARE_EMAIL=your_cloudflare_email
CLOUDFLARE_API_KEY=your_cloudflare_api_key
```
- `CLOUDFLARE_ZONE_ID`: Your Cloudflare Zone ID.
- `CLOUDFLARE_EMAIL`: Your Cloudflare account email.
- `CLOUDFLARE_API_KEY`: Your Cloudflare API key.

**Note**: `CLOUDFLARE_ZONE_ID` can be passed as the argument `zone-id`. In this case, it takes priority over the environment variable."

### OVH Configuration
```env
OVH_ENDPOINT=your_endpoint
OVH_APPLICATION_KEY=your_application_key
OVH_APPLICATION_SECRET=your_application_secret
OVH_CONSUMER_KEY=your_consumer_key
```
- `OVH_ENDPOINT`: Your OVH endpoint. [This is a list](https://github.com/ovh/python-ovh#2-configure-your-application) of available endpoints.
- `OVH_APPLICATION_KEY`: Your OVH Application key.
- `OVH_APPLICATION_SECRET`: Your OVH Application secret.
- `OVH_CONSUMER_KEY`: Your OVH Consumer key.

These `OVH_APPLICATION_KEY`, `OVH_APPLICATION_SECRET and `OVH_CONSUMER_KEY` could be created by [creation page](https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*).

## Development
### Adding New Providers
The script is designed to be easily extensible. To add support for a new provider:
1. Create a new class that inherits from `Provider` (defined in `factories/providers/providers.py`). Implement the `get` and `update` methods to interact with the new provider's API.
2. Create a corresponding `ProviderCreator` class (inheriting from `factories/providers/creators.py`) to create instances of your new provider class.
3. Update the `main.py` to recognize your new provider name.
4. Create a new `EnvironmentBuilder` for the provider if it requires different configuration settings.

Be free to open a feature or bugfix branch, then a PR; I'm pleased to accept it!
I suggest that you use [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/).

### Development Tools
The project uses several development tools for code quality and type checking:

1. Run Ruff for code linting:
    ```bash
    make lint
    ```

2. Run Ruff for code formatting:
    ```bash
    make format
    ```
   
3. Run mypy for static type checking:
    ```bash
    make type-check
    ```

It's recommended to run these tools before committing changes to ensure code quality and consistency.

## Log - Expected Output Messages
1. Record not found:
```
[YYYY-MM-DD HH:MM:SS] - ERROR: Record '<record_name>' not found.
```
2. IP changed:
```
[YYYY-MM-DD HH:MM:SS] - INFO: Record updated successful for '<record_name>'.
```
3. IP same:
```
[YYYY-MM-DD HH:MM:SS] - INFO: Record not updated for '<record_name>' because hasn't changed.
```
4. Update failed:
```
[YYYY-MM-DD HH:MM:SS] - ERROR: Record update failed for '<record_name>' with these reasons: ['Error message'].
```

## Notes
- The script modifies the DNS record's IP address.
- Ensure your API credentials have the necessary permissions.
- The public IP is fetched using the ipify API.
- Logs are stored in the `logs` directory.
- The Builder pattern is used for environment configuration.
- The Factory Method pattern is used to add a new provider.
- The code is well-documented.
 
## License
MIT License.

This version emphasizes the generic nature of the solution and provides clear instructions on how to extend it with new providers. It also clarifies the configuration process and expected output in a more general way.
