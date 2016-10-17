import logging


def setup_logger(logger_name, log_file, fmt='@%(levelname)s %(asctime)s %(message)s', datefmt='[%d/%m/%y] [%I:%M:%S %p]', level=logging.INFO, propagate=False, stream=True):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(formatter)
    l.addHandler(fileHandler)

    if stream:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.addHandler(streamHandler)

    l.setLevel(level)
    l.propagate = propagate


def load_token():
    with open('token') as f:
        token = f.read().strip()
    return token
