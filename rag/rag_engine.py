from rag.knowledge_base import medical_knowledge
from rag.vector_store import VectorStore

class RAGEngine:

    def __init__(self):

        self.vector_store = VectorStore(medical_knowledge)

    def generate_explanation(self, prediction):

        if prediction == 1:
            query = "heart disease risk factors"
        else:
            query = "healthy heart lifestyle"

        docs = self.vector_store.search(query)

        explanation = " ".join(docs)

        return explanation

    def get_context(self, message):
        docs = self.vector_store.search(message)
        return " ".join(docs)