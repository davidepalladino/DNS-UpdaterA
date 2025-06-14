# DNS-UpdaterA
This script provides a framework for managing DNS records across different providers. It's designed:
- to be Docker-less, this is useful to have a lightweight solution.
- with a modular architecture that allows you to easily add support for new DNS providers.

The current implementation includes support for Cloudflare.

## Features
- **Provider-Agnostic Design:** The core logic for fetching the public IP and updating DNS records is abstracted, allowing easy integration with various DNS providers.
- **Pluggable Providers:**  New DNS providers can be added by implementing a simple interface, without modifying the core logic. This is possible of Factory Method pattern.
- **Robust Error Handling:** Comprehensive error handling for API requests, environment variables, and argument parsing.
- **Detailed Logging:**  Logging with daily rotation and backups.
- **Well-Documented Code:**  Docstrings for all classes and functions.
- **Builder Pattern:**  Uses the Builder pattern for flexible environment configuration.

## Requirements
- Python 3.7 or higher.
- The following Python modules:
    - `requests`
    - `python-dotenv`
    - `logging`
    - `typing`
    - `ovh`

## Installation 
1. Clone or download this repository.
2. Install the required Python dependencies using `pip`:

```bash
pip install requests python-dotenv ovh
```
or
```bash
pip install -r requirements.txt 
```
3. Create a `.env` file in the script directory with the required environment variables as described in the Configuration section.

### Configuration
The configuration process depends on the chosen DNS provider. The script uses environment variables for authentication and other provider-specific settings.

#### Cloudflare Configuration
```env
CLOUDFLARE_ZONE_ID=your_zone_id
CLOUDFLARE_EMAIL=your_cloudflare_email
CLOUDFLARE_API_KEY=your_cloudflare_api_key
```
- `CLOUDFLARE_ZONE_ID`: Your Cloudflare Zone ID.
- `CLOUDFLARE_EMAIL`: Your Cloudflare account email.
- `CLOUDFLARE_API_KEY`: Your Cloudflare API key.

**Note**: `CLOUDFLARE_ZONE_ID` can be passed as the argument `zone-id`. In this case, it takes priority over the environment variable."

#### OVH Configuration
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

## Usage
Run the script, specifying the provider and record name:
```bash
python main.py --provider <provider> --name <record_name> [--zone-id <cloudflare_zone_id>]
```

## Adding New Providers (for developers)
The script is designed to be easily extensible. To add support for a new provider:
1. Create a new class that inherits from `Provider` (defined in `factories/providers/providers.py`). Implement the `get` and `update` methods to interact with the new provider's API.
2. Create a corresponding `ProviderCreator` class (inheriting from `factories/providers/creators.py`) to create instances of your new provider class.
3. Update the `main.py` to recognize your new provider name.
4. Create a new `EnvironmentBuilder` for the provider if it requires different configuration settings.

Be free to open feature or bugfix branch, then a PR; I'm pleased to accept it!
I suggest you to use [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/).

## Expected Output
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
- The Factory Method pattern is used to add new provider.
- The code is well-documented.
 
## License
MIT License.

This version emphasizes the generic nature of the solution and provides clear instructions on how to extend it with new providers. It also clarifies the configuration process and expected output in a more general way.
