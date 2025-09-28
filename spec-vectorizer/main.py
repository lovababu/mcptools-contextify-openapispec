import logging
from utils.yaml_ops import read_yaml
from processor.spec_split import build_spec_documents
from db.crud import store_specs

logging.basicConfig(
    level=logging.INFO,  # Set the minimum logging level to INFO
    format='%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Test Logger")
    # ideally implementation should be clone the spec repo and process each and every yaml file.
    yaml_dict = read_yaml(spec_url="https://raw.githubusercontent.com/swagger-api/swagger-petstore/refs/heads/master/src/main/resources/openapi.yaml")

    # Separate the OpenAPI specification by URL paths so each path can be stored as an individual chunk in the vector database.
    # In case of chunk size is too long, we can think of splitting specification by URL path & method.
    docs_by_path_and_method = build_spec_documents(api_spec=yaml_dict)
    doc_ids = store_specs(docs_by_path_and_method)
    print("Document ids stored in database: ", doc_ids)
