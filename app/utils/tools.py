from logging import DEBUG, FileHandler, Formatter, Logger, getLogger


def make_logger(log_name):

    logger_: Logger = getLogger(log_name)
    logger_.setLevel(DEBUG)

    fh = FileHandler(f'{log_name}.log')
    fh.setLevel(DEBUG)

    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger_.addHandler(fh)

    return logger_
