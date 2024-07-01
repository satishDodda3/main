import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.BaseModel import BaseModel
import utils as ut
import configparser
import requests

class Cortical(BaseModel):
    def __init__(self,name):
        self.name = name
        self.auth_token = ut.get_config_value('cortical','api_key')
        self.compare_url = ut.get_config_value('cortical','compare_url')
    def similarity(self,inputs):
        headers = {
            "Authorization": self.auth_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data = [
            {"text": ut.get_synonyms(inputs[0]), "language": "en"},
            {"text": ut.get_synonyms(inputs[1]), "language": "en"}
        ]
        self.response = requests.post(self.compare_url, headers=headers, json=data)
        return self.__get_similarty_score()
    
    def __get_similarty_score(self):
        if self.response.status_code == 200:
            response_data = self.response.json()
            similarity = response_data.get('similarity', None)
            return similarity
        else:
            raise Exception() 