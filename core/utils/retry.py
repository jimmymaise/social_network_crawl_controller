from tenacity import *  # noqa: F403

from core.logger.logger_handler import Logger


def warning_when_retry(attempt, sleep, last_result):
    logger = Logger.get_logger()
    logger.warning(
        f'Retrying attempt {last_result.attempt_number} ended with exception {getattr(last_result, "_exception")}')


def decorate(*args, **kwargs):
    return retry(*args, **kwargs)  # noqa: F405


def return_last_value(retry_state):
    """return the result of the last call attempt"""
    return retry_state.outcome.result()
