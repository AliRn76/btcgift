from kavenegar import APIException, HTTPException
from config.exceptions import KavenegarException
from config.settings import KAVENEGAR
import logging


logger = logging.getLogger('root')


def send_otp_sms(phone_number, otp, option='sms'):
    param = {
        'token': otp,
        'receptor': [f'0{phone_number}'],
        'template': 'otp',
        'type': option
        # Default Is SMS
    }
    try:
        KAVENEGAR.verify_lookup(param)
        logger.error(f'[OTP] Sent Successfully | {phone_number} --> {otp}')
    except (APIException, HTTPException) as e:
        logger.error(f'[OTP] Request Exception | {e}')
        raise KavenegarException
