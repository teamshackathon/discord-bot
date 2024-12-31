import json
import os
from abc import ABCMeta, abstractmethod


class Config(metaclass=ABCMeta):

    def __init__(self, env):
        self.env = env

    @abstractmethod
    def get_discord_bot_token(self):        
        raise NotImplementedError()
    

class DevelopmentConfig(Config):
    
    def __init__(self):
        super().__init__('development')
        
        with open('secrets.json', encoding='utf-8') as f:
            data = json.load(f)

        self.data = data['development']

    def get_discord_bot_token(self):
        return self.data['discord_bot_token']
    
    def get_gemini_api_key(self):
        return self.data['gemini_api_key']
    
    def get_prompt(self, prompt):
        return f"{self.data['default_prompt']['start']} {prompt} {self.data['default_prompt']['end']}"
    
    def get_dbstring(self, ):
        return f"host={self.data['postgres']['host']} port={self.data['postgres']['port']} dbname={self.data['postgres']['dbname']} " \
        f"user={self.data['postgres']['user']} password={self.data['postgres']['password']}"
    

class ProductionConfig(Config):

    def __init__(self):
        super().__init__('production')
        self.data = {
            'discord_bot_token': os.environ['BOT_TOKEN'],
            'gemini_api_key': os.environ['GEMINI_API_KEY'],
            'postgres': {
                'host': os.environ['POSTGRES_HOST'],
                'port': os.environ['POSTGRES_PORT'],
                'dbname': os.environ['POSTGRES_DB'],
                'user': os.environ['POSTGRES_USER'],
                'password': os.environ['POSTGRES_PASSWORD']
            },
            "default_prompt": {
            "start": "",
            "end": "最後に私は日本人なので、日本語で解答してくださると幸いです。いつもありがとうございます。"}
        }

    def get_discord_bot_token(self):
        return self.data['discord_bot_token']
    
    def get_gemini_api_key(self):
        return self.data['gemini_api_key']
    
    def get_prompt(self, prompt):
        return f"{self.data['default_prompt']['start']} {prompt} {self.data['default_prompt']['end']}"
    
    def get_dbstring(self, ):
        return f"host={self.data['postgres']['host']} port={self.data['postgres']['port']} dbname={self.data['postgres']['dbname']} " \
        f"user={self.data['postgres']['user']} password={self.data['postgres']['password']}"
        