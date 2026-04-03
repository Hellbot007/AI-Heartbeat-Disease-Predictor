from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:

    def __init__(self, documents):

        self.documents = documents
        self.vectorizer = TfidfVectorizer()

        self.doc_vectors = self.vectorizer.fit_transform(documents)

    def search(self, query, top_k=2):

        query_vec = self.vectorizer.transform([query])

        similarity = cosine_similarity(query_vec, self.doc_vectors)

        top_indices = similarity.argsort()[0][-top_k:]

        results = [self.documents[i] for i in top_indices]

        return results