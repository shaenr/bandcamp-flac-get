import logging
from pathlib import Path

TEST_LOG_LEVEL = 1
TEST_LOG_FILE = "log.txt"
PROJECT_NAME = "shaen_logger"


def create_log_file(log_file):
    path = _log_file_path_resolver(log_file)
    try:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch()
    except IsADirectoryError:
        slog.error(f"{path} is a directory... Cannot touch.")


def _log_file_path_resolver(log_file: str):
    return Path(f"./{PROJECT_NAME}/.logs/{log_file}").resolve()


def new_logger(log_file: str = TEST_LOG_FILE,
               log_level: int = TEST_LOG_LEVEL) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level * 10)  # logging.DEBUG
    create_log_file(log_file)
    file_handler = logging.FileHandler(
        _log_file_path_resolver(log_file)
    )
    formatter = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def get_slog():
    return logging.getLogger(__name__)


def set_log_level(log_level):
    logger = get_slog()
    logger.setLevel(log_level)


def print_output():
    slog.debug('A debug message')
    slog.info('An info message')
    slog.warning('Something is not right.')
    slog.error('A Major error has happened.')
    slog.critical('Fatal error. Cannot continue')
    zero_divide_exception(21, 0)


def zero_divide_exception(x: int = 21, y: int = 0):
    try:
        out = x / y
    except ZeroDivisionError:
        slog.exception("Division by zero problem")


if __name__ != "__main__":
    # slog = new_logger()
    slog = get_slog()

