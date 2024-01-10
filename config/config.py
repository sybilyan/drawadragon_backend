


import sys
import json

class ServiceConfig:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.args = sys.argv[1:]

            # load config file
            cls._instance.all_configs = {}
            cls._instance._load_config()

            # get config
            assert len(cls._instance.args) > 0
            cls._instance.which_config = cls._instance.args[0]

            assert cls._instance.which_config in cls._instance.all_configs
            cls._instance.config = cls._instance.all_configs.get(cls._instance.which_config, {})
        return cls._instance
    

    def _load_config(self):
        with open('config/config.json') as config_file:
            self.all_configs = json.loads(config_file.read())

    def __getitem__(self, key):
        return self.config[key]
    
    def __contains__(self, key):
        return key in self.config


CONFIG = ServiceConfig()
