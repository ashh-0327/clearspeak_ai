import chromadb
from sentence_transformers import SentenceTransformer
from services.knowledge_base import LEGAL_KNOWLEDGE

chroma_client = chromadb.PersistentClient(path='data/chroma_db')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_or_create_collection():
    collection = chroma_client.get_or_create_collection(
        name='legal_knowledge',
        metadata={'hnsw:space': 'cosine'}
    )
    return collection

def build_knowledge_base():
    collection = get_or_create_collection()
    if collection.count() > 0:
        print('Knowledge base already exists with ' + str(collection.count()) + ' entries.')
        return
    print('Building legal knowledge base...')
    texts = [item['term'] + ': ' + item['definition'] for item in LEGAL_KNOWLEDGE]
    embeddings = embedding_model.encode(texts).tolist()
    ids = [item['id'] for item in LEGAL_KNOWLEDGE]
    metadatas = [{'domain': item['domain'], 'term': item['term']} for item in LEGAL_KNOWLEDGE]
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    print('Knowledge base built with ' + str(len(LEGAL_KNOWLEDGE)) + ' legal terms.')

def retrieve_relevant_context(query_text, domain=None, top_k=5):
    collection = get_or_create_collection()
    if collection.count() == 0:
        build_knowledge_base()
    query_embedding = embedding_model.encode([query_text]).tolist()
    where_filter = {'domain': domain} if domain else None
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        where=where_filter,
        include=['documents', 'metadatas', 'distances']
    )
    context_parts = []
    for i, doc in enumerate(results['documents'][0]):
        distance = results['distances'][0][i]
        if distance < 0.8:
            context_parts.append('- ' + doc)
    if context_parts:
        return 'Relevant legal definitions:\n' + '\n'.join(context_parts)
    else:
        return ''
