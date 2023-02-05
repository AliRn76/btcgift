from kavenegar import APIException, HTTPException
from config.exceptions import KavenegarException
from config.settings import KAVENEGAR
from config.utils import log_info, log_error


def send_otp_sms(phone_number, otp, option='sms'):
    param = {
        'token': otp,
        'receptor': [f'0{phone_number}'],
        'template': 'otp',
        'type': option
        # Default Is SMS
    }
    try:
        # KAVENEGAR.verify_lookup(param)
        log_info('OTP', title='Sent Successfully', message=f'{phone_number} --> {otp}')
    except (APIException, HTTPException) as e:
        log_error('OTP', title='Request Exception', message=e)
        raise KavenegarException
