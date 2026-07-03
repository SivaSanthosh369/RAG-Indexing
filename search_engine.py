# search_engine.py

def get_relevant_chunks(query, chunks_with_pages, top_k=3):
    query_words = set(query.lower().split())
    scored_chunks = []
    
    for item in chunks_with_pages:
        score = sum(1 for word in query_words if word in item["text"].lower())
        scored_chunks.append((score, item))
        
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored_chunks[:top_k] if score > 0]


def format_bionic_text(text):
    formatted_words = []
    for word in text.split():
        if len(word) > 3 and not word.startswith("http"):
            mid = len(word) // 2
            formatted_words.append(f"**{word[:mid]}**{word[mid:]}")
        else:
            formatted_words.append(word)
    return " ".join(formatted_words)