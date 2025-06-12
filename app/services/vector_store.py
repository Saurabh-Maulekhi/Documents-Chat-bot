from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv

def create_vector_store(chunks, metadata):
    """"
    chunks: a list of text segments
    metadata: associated metadata for each chunk
    """
    
    embeddings = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_texts(chunks, embeddings, metadatas=metadata, persist_directory="vectordb")
    vectordb.persist() # Saves the vector store to disk at the specified persist_directory ("vectordb") to allow future retrieval without recomputing embeddings.
    return vectordb


def load_vector_store():
    """
    load a previously created vector store.
    """
    
    embeddings = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

    return Chroma(persist_directory="vectordb", embedding_function=embeddings)
