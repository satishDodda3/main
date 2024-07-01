import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.BaseModel import BaseModel
import utils as ut
from sentence_transformers import SentenceTransformer, util


class Transfromer(BaseModel):
    def __init__(self,name):
        self.name = name

    def initialize_model(self):
        return SentenceTransformer(self.name)
    
    def similarity(self,inputs):
         model=self.initialize_model()
         first_word_list=ut.get_synonyms(inputs[0])
         second_word_list=ut.get_synonyms(inputs[1])
         first = model.encode(first_word_list, convert_to_tensor=True)
         second = model.encode(second_word_list, convert_to_tensor=True)
         similarity_score = util.pytorch_cos_sim(first,second).item()
         
         return  similarity_score
    
    