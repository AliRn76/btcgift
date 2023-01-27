import re


def validate_phone_number(phone_number):
    if match := re.match(r'^(\+98|98|0)?(9\d{9})$', phone_number):
        return match.groups()[1]
    else:
        return None


def client_ip(context):
    return context['request'].META.get('REMOTE_ADDR')
