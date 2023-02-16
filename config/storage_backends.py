from storages.backends.s3boto3 import S3StaticStorage


class StaticStorage(S3StaticStorage):
    location = 'static'


class MediaStorage(S3StaticStorage):
    querystring_auth = False
    location = 'media'
