import yaml

def load_configs_from_file(filename='config.yaml'):
    _config_stream = open(filename, 'r')
    return yaml.safe_load(_config_stream) 