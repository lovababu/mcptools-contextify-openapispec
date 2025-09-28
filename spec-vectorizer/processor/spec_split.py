import yaml
import logging
import json


logger = logging.getLogger(__name__)

def _split_api_spec_by_path_and_method(yaml_data: dict) -> list[dict]:
    """
    Splits an OpenAPI specification dictionary into multiple dictionaries,
    each containing the full spec for a single path.
    Args:
        yaml_data (dict): The OpenAPI specification as a dictionary.
    Returns:
        list[dict]: A list of dictionaries, each representing the OpenAPI spec for one path.
    """
    paths = yaml_data.get('paths', {})
    logger.info(f"Number of paths in a spec: {len(paths) if paths else 0}")
    specs_by_path = []
    http_methods = ['put', 'post', 'get', 'delete', 'options']
    if paths:
        for path, path_spec in paths.items():
            for method in http_methods:
                if method in path_spec:
                    spect_by_req_method = {k: v for k, v in yaml_data.items() if k != 'paths'}
                    spect_by_req_method['paths'] = {path: {method: path_spec[method]}}
                    specs_by_path.append(spect_by_req_method)
    return specs_by_path

def _build_id(spec: dict):
    id_tokens = []
    # Add the first server URL if available
    servers = spec.get('servers')
    if servers and isinstance(servers, list) and servers and 'url' in servers[0]:
        id_tokens.append(servers[0]['url'])
    # Add path and HTTP method
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        id_tokens.append(path)
        if isinstance(methods, dict):
            for method in methods.keys():
                id_tokens.append(method)
    # Join tokens and sanitize
    return "_".join(id_tokens).replace("/", "_").replace(":", "_")
    
def _build_metadata(spec: dict):
    metadata = {}
    info = spec.get('info', {})
    if 'title' in info:
        metadata['title'] = info['title']
    if 'description' in info:
        metadata['description'] = info['description']
    if 'version' in info:
        metadata['version'] = info['version']

    paths = spec.get('paths', {})
    # Since each spec is for a single path and method, extract them
    if paths:
        for path, methods in paths.items():
            metadata['path'] = path
            if isinstance(methods, dict):
                for method in methods.keys():
                    metadata['method'] = method
    return metadata

def build_spec_documents(api_spec: dict):
    documents = []

    for yaml_dict in _split_api_spec_by_path_and_method(yaml_data=api_spec):
        document = {
            'id': _build_id(yaml_dict),
            'metadata': _build_metadata(yaml_dict),
            'content': json.dumps(yaml_dict)
        }
        documents.append(document)
    return documents

