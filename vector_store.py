# vector_store.py
import chromadb
import ollama

# PersistentClient connects to a local database stored in the specified path
chroma_client = chromadb.PersistentClient(path="./RAG_db")

collection = chroma_client.get_or_create_collection(name="adhd_focus_rag")

def get_ollama_embedding(text):
    """Convert text to a vector embedding"""
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

def add_chunks_to_vector_db(chunks_with_pages):
    """Add all chunks with their page/timestamp to the vector database"""

    try:
        chroma_client.delete_collection(name="adhd_focus_rag")
    except:
        pass
    
    global collection
    collection = chroma_client.get_or_create_collection(name="adhd_focus_rag")
    
    ids = [f"id_{i}" for i in range(len(chunks_with_pages))]
    embeddings = [get_ollama_embedding(item["text"]) for item in chunks_with_pages]
    documents = [item["text"] for item in chunks_with_pages]
    metadatas = [{"page": str(item["page"])} for item in chunks_with_pages]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

def query_vector_db(query, top_k=3):
    """Query the vector database for relevant chunks (Semantic Search)"""
    query_embedding = get_ollama_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    formatted_results = []
    if results and results["documents"]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            formatted_results.append({
                "text": doc,
                "page": meta["page"]
            })
    return formatted_results