
import time
import yaml
import sys


stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
last_log_is_progress = False

def logger(message, progress_indicator = False):
    global last_log_is_progress

    if progress_indicator:
        if not last_log_is_progress:
            last_log_is_progress = True
            sys.stdout.write('\n => .')
            sys.stdout.flush()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
        return

    if last_log_is_progress:
        sys.stdout.write('\n\n')
        sys.stdout.flush()
        last_log_is_progress = False

    datetime = time.localtime()
    formatted_datetime = time.strftime("%d/%m/%Y %H:%M:%S", datetime)
    formatted_message = "[{}] \n => {} \n\n".format(formatted_datetime, message)
    print(formatted_message)

    if (c['save_log_to_file'] == True):
        logger_file = open("logger.log", "a")
        logger_file.write(formatted_message)
        logger_file.close()

    return True