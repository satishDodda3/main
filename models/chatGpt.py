import sys,os
from openai import OpenAI
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.BaseModel import BaseModel
import utils as ut
import numpy as np

class ChatGpt(BaseModel):
    def __init__(self,name):
        self.name = name
        self.api_key=ut.get_config_value('chatGpt','api_key')
        self.client = OpenAI(api_key=self.api_key)
    def get_embeddings(self, text, model=ut.get_config_value('chatGpt','model_1')):
        response = self.client.embeddings.create(input=text, model=model)
        return response.data[0].embedding

    def calculate_cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        return dot_product / (magnitude1 * magnitude2)

    def similarity(self,inputs):
        source_key_synonyms = ut.get_synonyms(inputs[0])
        target_key_synonyms = ut.get_synonyms(inputs[1])

        source_key_vec = self.get_embeddings(source_key_synonyms)
        target_key_vec = self.get_embeddings(target_key_synonyms)
        cosine_similarity = self.calculate_cosine_similarity(source_key_vec, target_key_vec)
        return cosine_similarity
        
        