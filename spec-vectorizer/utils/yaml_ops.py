import yaml
import logging
import requests
import time
from functools import wraps

logger = logging.getLogger(__name__)

def time_download(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Time taken to download file: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@time_download
def _load_yaml(url_path: str):
    """
    Fetches and decodes YAML content from the specified URL.
    Args:
        url_path (str): The URL to fetch the YAML content from.
    Returns:
        str: The decoded YAML content as a string.
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        requests.exceptions.RequestsDependencyWarning: If there is a dependency warning during the request.
    Logs:
        Info: Successful loading of YAML content.
        Error: Any issues encountered during the request.
    """
    
    try:
        response = requests.get(url=url_path, allow_redirects=True)
        response.raise_for_status()
        yaml_content = response.content.decode("utf-8")
        logger.info(f"Yaml content from the url {url_path} loaded successfully.")
        return yaml_content
    except requests.exceptions.RequestsDependencyWarning as re:
        logger.error(f"Requests dependency warning while loading yaml from url: {url_path}", exc_info=re)
    
        
def read_yaml(spec_url: str) -> dict[any, any]:
    """
    Loads and parses a YAML file from the given URL or file path.
    Args:
        spec_url (str): The URL or file path to the YAML file.
    Returns:
        dict: Parsed YAML data as a Python dictionary if successful, otherwise None.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """

    try:
        yaml_content = _load_yaml(url_path=spec_url)
        data = yaml.safe_load(yaml_content)
        #logger.info(f"YAML data loaded: {data}")
        return data
    except FileNotFoundError as fne:
        logging.error(f"Error while loading yaml file: {spec_url}", exc_info=fne)
    except yaml.YAMLError as ye:
        logging.error(f"YAML error while parsing file: {spec_url}", exc_info=ye)