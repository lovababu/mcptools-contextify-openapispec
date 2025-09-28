from db import chroma_client
from langchain_core.documents import Document

def _build_chroma_document(spec_docs: list[dict[any, any]]):
    documents = []
    ids = []
    for item in spec_docs:
        documents.append(Document(page_content=item['content'], 
                                  metadata=item['metadata'], id=item['id']))
        ids.append(item['id'])
    return ids, documents

def store_specs(specs: list[dict[any, any]]) -> list[str]:
    ids, documents = _build_chroma_document(spec_docs=specs)
    doc_ids = chroma_client.add_documents(
        documents=documents,
        ids=ids
    )
    return doc_ids
    

def query_vector(meta_data: dict, search_text: str):
    pass
