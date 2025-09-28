from chromadb import HttpClient
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

http_client = HttpClient(host="0.0.0.0", port=8000, ssl=False)
model_name = "mxbai-embed-large:latest"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
ollamma_embeddings = OllamaEmbeddings(
    model=model_name,
    base_url="http://localhost:11434",
    validate_model_on_init=True
)

chroma_client = Chroma(
    client=http_client,
    collection_name= "open_api_spec_vectors",
    embedding_function=ollamma_embeddings
)

all_docs = chroma_client.get()
print(all_docs)


