import src.env as env

def forceFullScreenForThis(fn):
    def exec(*args, **kwargs):
        env.force_full_screen = True
        result = fn(*args, **kwargs)
        env.force_full_screen = False
        return result
    return exec