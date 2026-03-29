# run_rag.py
from src.rag.retriever import PolicyKnowledgeBase

if __name__ == "__main__":
    doc_path = "data/raw/lending_policies.txt"
    
    # Initialize our RAG system
    rag_system = PolicyKnowledgeBase()
    
    # 1. Build the DB (you only need to do this once when documents change)
    rag_system.build_knowledge_base(document_path=doc_path)
    
    # 2. Test the retrieval engine with a natural language query
    test_query = "What happens if a borrower misses payments for more than 90 days?"
    rag_system.retrieve_context(query=test_query)
    
    print("\n" + "="*50)
    
    test_query_2 = "What is the fraud threshold for someone with a 500 credit score?"
    rag_system.retrieve_context(query=test_query_2)