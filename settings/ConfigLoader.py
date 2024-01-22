import json


class ConfigLoader:

    def __init__(self):
        with open("conf/conf.json", 'r') as file:
            self.config = json.load(file)

    def get_config(self):
        return self.config
