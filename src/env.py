from src.utils.assets import loadImages, loadHeroesImagesToHome
from src.utils.config import loadConfigsFromFile
from src.bot.logger import logger

logger('Setting up global variables...', color='green')
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
global multi_account_same_monitor
global force_full_screen
global mouse_move_speed
global in_login_process
global debug

logger('Setting up default values for variables...', color='green')
window_object = None
login_attempts = 0
hero_clicks = 0
last_log_is_progress = False
images = []
home_heroes = []
force_full_screen = False
in_login_process = False

cfg = loadConfigsFromFile()

logger('Mapping configs...', color='green')
threshold = cfg['threshold']
home = cfg['home']
scale_image = cfg['scale_image']
multi_account_same_monitor = cfg['multiples_accounts_same_monitor']
mouse_move_speed = cfg['mouse_move_speed']
debug = cfg['debug']

logger('Loading assets...', color='green')
images = loadImages()
if home['enable']:
    logger('HOME Enabled. Loading heroes assets...', color='green')
    home_heroes = loadHeroesImagesToHome()
