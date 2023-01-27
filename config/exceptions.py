from rest_framework.exceptions import APIException


class KavenegarException(APIException):
    status_code = 409
    default_detail = 'مشکلی در ارسال پیام کوتاه پیش آمده است'
