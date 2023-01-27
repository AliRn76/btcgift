import random
import re

from config.settings import OTP_LEN


def validate_phone_number(phone_number):
    if match := re.match(r'^(\+98|98|0)?(9\d{9})$', phone_number):
        return match.groups()[1]
    else:
        return None


def client_ip(context):
    return context['request'].META.get('REMOTE_ADDR')


def generate_otp():
    return random.randint(10**(OTP_LEN-1), (10**OTP_LEN)-1)
