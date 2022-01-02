import yaml

def loadConfigsFromFile(filename='config.yaml'):
    _config_stream = open(filename, 'r')
    return yaml.safe_load(_config_stream) 