import src.env as env

def inLoginProcess(fn):
    def exec(*args, **kwargs):
        env.in_login_process = True
        result = fn(*args, **kwargs)
        env.in_login_process = False
        return result
    return exec