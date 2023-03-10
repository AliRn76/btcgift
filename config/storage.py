import boto3
import logging
from botocore.exceptions import ClientError

# from dotenv import dotenv_values
# # from config.settings import STORAGE_ENDPOINT_URL, STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY, BUCKET_NAME
# env = dotenv_values('/home/ali/dev/btcgift/.env')
# STORAGE_ENDPOINT_URL = env['STORAGE_ENDPOINT_URL']
# STORAGE_MEDIA_URL = env['STORAGE_MEDIA_URL']
# STORAGE_ACCESS_KEY = env['STORAGE_ACCESS_KEY']
# STORAGE_SECRET_KEY = env['STORAGE_SECRET_KEY']
# BUCKET_NAME = env['BUCKET_NAME']


logger = logging.getLogger('root')

# s3_resource = boto3.resource(
#     's3',
#     endpoint_url=STORAGE_ENDPOINT_URL,
#     aws_access_key_id=STORAGE_ACCESS_KEY,
#     aws_secret_access_key=STORAGE_SECRET_KEY,
# )
# s3_client = boto3.client(
#     's3',
#     endpoint_url=STORAGE_ENDPOINT_URL,
#     aws_access_key_id=STORAGE_ACCESS_KEY,
#     aws_secret_access_key=STORAGE_SECRET_KEY,
# )


def list_buckets():
    try:
        for bucket in s3_resource.buckets.all():
            logger.info(f'bucket_name: {bucket.name}')
    except ClientError as exc:
        logger.error(exc)


def get_bucket_cors():
    try:
        response = s3_client.get_bucket_cors(Bucket=BUCKET_NAME)
        logging.info(response['CORSRules'])
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
            return []
        else:
            # AllAccessDisabled error == bucket not found
            logger.error(e)


def upload_object(file_path: str, private: bool = False) -> str:
    try:
        bucket = s3_resource.Bucket(BUCKET_NAME)
        object_name = file_path[file_path.rfind('/') + 1:]  # nft.webp
        with open(file_path, "rb") as file:
            bucket.put_object(
                ACL='private' if private else 'public-read',
                Body=file,
                Key=object_name
            )
        return f'/{object_name}'
    except ClientError as e:
        logger.error(e)


def objects_list():
    try:
        bucket = s3_resource.Bucket(BUCKET_NAME)

        for obj in bucket.objects.all():
            print(obj)
            logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")

    except ClientError as e:
        logger.error(e)


# upload_object(file_path='/home/ali/dev/btcgift/media/blog/mining.jpg')
# 'https://btcgift.s3.ir-thr-at1.arvanstorage.com/mining.jpg'
# objects_list()

