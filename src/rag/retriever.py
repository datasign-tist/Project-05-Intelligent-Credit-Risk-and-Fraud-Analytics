import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class PolicyKnowledgeBase:
    def __init__(self, persist_directory: str = "data/chroma_db"):
        self.persist_directory = persist_directory
        # Using a fast, local embedding model that runs easily on a Mac
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def build_knowledge_base(self, document_path: str):
        """Loads text, chunks it, embeds it, and saves to ChromaDB."""
        print(f"Loading document from {document_path}...")
        loader = TextLoader(document_path)
        documents = loader.load()

        # Split the document into smaller chunks for the Vector DB
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, 
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(documents)

        print(f"Creating vector database with {len(chunks)} embedded chunks...")
        # This automatically persists to the directory specified
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        print(f"Knowledge base built and saved to {self.persist_directory}!")

    def retrieve_context(self, query: str, k: int = 2):
        """Searches the vector database for the most relevant policy chunks."""
        # Load the DB if it's not already in memory
        if not self.vector_store:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        
        print(f"\n[QUERY]: '{query}'")
        # Perform a similarity search in the vector space
        results = self.vector_store.similarity_search(query, k=k)
        
        contexts = []
        for i, doc in enumerate(results):
            contexts.append(doc.page_content)
            print(f"\n--- Relevant Policy Match {i+1} ---")
            print(doc.page_content)
            
        return contexts