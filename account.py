class Account:

    def __init__(self, window, index):
        self.index = index
        self.window = window
        self.last = {
            "login": 0,
            "heroes": 0,
            "all_heroes": 0,
            "new_map": 0,
            "check_for_captcha": 0,
            "refresh_heroes": 0,
            "interactive": 0,
        }