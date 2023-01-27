from kavenegar import APIException, HTTPException
from config.exceptions import KavenegarException
from config.settings import KAVENEGAR


def send_otp_sms(phone_number, otp, option='sms'):
    param = {
        'token': otp,
        'receptor': [f'0{phone_number}'],
        'template': 'otp',
        'type': option
        # Default Is SMS
    }
    try:
        response = KAVENEGAR.verify_lookup(param)
        print(response)
    except (APIException, HTTPException) as e:
        print(e)
        raise KavenegarException
