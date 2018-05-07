import json


class Config:
    _instance = None
    default_conf = 'config.json'

    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.server = data['server']
            self.token = data['token']
            self.crypto_salt = data['salt']
            self.is_webhook = data.get('mode') == 'server'
            if self.is_webhook:
                self.hook_url = data['webhook']['url']
                self.hook_key = data['webhook']['key']
        Config._instance = self

    @staticmethod
    def instance():
        if Config._instance is None:
            Config(Config.default_conf)
        return Config._instance

    @staticmethod
    def add_connection(connection):
        Config.instance().connection = connection

    @staticmethod
    def add_bot(bot):
        Config.instance().bot = bot

    @staticmethod
    def add_dispatcher(dp):
        Config.instance().dispatcher = dp

