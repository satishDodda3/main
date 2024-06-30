from openai import OpenAI 
import numpy as np
from nltk.corpus import wordnet as wn

class NLPProcessor:
    print("Satish Dodda")
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        print()

    def get_synonyms(self, key):
        source_key = ""
        source_key_wn = wn.synsets(key.replace(' ', "_"))
        if source_key_wn:
            source_key = "In the healthcare context, " + key + " has synonyms "
            synonyms = [lemma.name().replace("_", " ") for lemma in source_key_wn[0].lemmas()]
            source_key += ", ".join(synonyms)
            source_key += " and is defined as " + source_key_wn[0].definition()
        if not source_key:
            return key
        return source_key

    def get_embeddings(self, text, model="text-embedding-ada-002"):
        response = self.client.embeddings.create(input=text, model=model)
        return response.data[0].embedding

    def calculate_cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        return dot_product / (magnitude1 * magnitude2)

    def process(self, source_key, target_key):
        # Find synonyms
        source_key_synonyms = self.get_synonyms(source_key)
        target_key_synonyms = self.get_synonyms(target_key)

        # Get embeddings
        source_key_vec = self.get_embeddings(source_key_synonyms)
        target_key_vec = self.get_embeddings(target_key_synonyms)

        # Calculate cosine similarity
        cosine_similarity = self.calculate_cosine_similarity(source_key_vec, target_key_vec)
        return cosine_similarity
