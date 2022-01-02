import yaml
from src.utils import assets

def load_configs_from_file():
    _config_stream = open("config.yaml", 'r')
    return yaml.safe_load(_config_stream) 

def init():
    global window_object
    global threshold
    global home
    global cfg
    global scale_image
    global login_attempts
    global hero_clicks
    global last_log_is_progress
    global home_heroes
    global images

    # Default values for global vars
    window_object = None
    login_attempts = 0
    hero_clicks = 0
    last_log_is_progress = False
    images = []
    home_heroes = []

    cfg = load_configs_from_file()

    # Map configs
    threshold = cfg['threshold']
    home = cfg['home']
    scale_image = cfg['scale_image']

    # Load assets
    images = assets.load_images()
    if home['enable']:
        home_heroes = assets.loadHeroesToSendHome()
