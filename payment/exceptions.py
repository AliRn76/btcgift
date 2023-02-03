from rest_framework.exceptions import APIException


class GatewayException(APIException):
    status_code = 409
    default_detail = 'مشکلی در درگاه پرداخت پیش آمده است'
