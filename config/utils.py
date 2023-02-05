import re
import random
import logging
from config.settings import OTP_LEN


logger = logging.getLogger('root')


def validate_phone_number(phone_number):
    if match := re.match(r'^(\+98|98|0)?(9\d{9})$', phone_number):
        return match.groups()[1]
    else:
        return None


def client_ip(context):
    return context['request'].META.get('REMOTE_ADDR')


def generate_otp():
    return random.randint(10 ** (OTP_LEN - 1), (10**OTP_LEN) - 1)


def _clean_log_message(x: str, *, title: str, message: str) -> str:
    if len(title) < 10:
        tab = '\t\t\t'
    elif len(title) < 18:
        tab = '\t\t'
    elif len(title) < 26:
        tab = '\t'
    else:
        title = f'{title[:23]}...'
        tab = ''

    text = f'[{x}] {title}{tab}'
    if message:
        text += f'| {message}'
    return text


def log_info(x: str, *, title: str, message: str = None):
    text = _clean_log_message(x, title=title, message=message)
    logger.info(text)


def log_warning(x: str, *, title: str, message: str = None):
    text = _clean_log_message(x, title=title, message=message)
    logger.warning(text)


def log_error(x: str, *, title: str, message: str = None):
    text = _clean_log_message(x, title=title, message=message)
    logger.error(text)


def log_critical(x: str, *, title: str, message: str = None):
    text = _clean_log_message(x, title=title, message=message)
    logger.critical(text)
