import boto3
import os

from botocore.exceptions import ClientError

s3_resource = boto3.resource("s3", aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY_SECRET"), region_name=os.environ.get("AWS_REGION"))
s3_client = boto3.client("s3", aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY_SECRET"), region_name=os.environ.get("AWS_REGION"))

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

def read_s3_object(bucket_name, object):
    try:
        return s3_resource.Bucket(bucket_name).Object(object).get()['Body'].read()
    except:
        print(object + " does not exist in " + bucket_name)
        return None

def list_s3_objects(bucket_name, prefix):
    return s3_client.list_objects(
        Bucket=bucket_name,
        Prefix=prefix
    )