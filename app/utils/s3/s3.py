
import boto3
from botocore.exceptions import ClientError

from app.core.consts import AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name=AWS_DEFAULT_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

def download_file(s3_client, bucketName, key: str):
    try:
        return s3_client.Object(
            bucketName, key
        ).get()['Body'].read()
    except ClientError as err:
        print(f'Credential error => {err}')

def upload_file(s3_client, file, bucket, folder, object_name=None):
    # If S3 object_name was not specified, use file_name
    print("s3_client :" + s3_client + ", file  :" +  file + ", bucket :"+ bucket +", folder"+ folder)

    if object_name is None:
        object_name = file
    print("object_name", object_name)
    try:
        # 1
        #file = io.BytesIO(b'my data stored as file object in RAM')
        # with open("files", "rb") as f:
        s3_upload_file = s3_client.upload_fileobj(
            file,
            #"app1-public-s3-dev",
            bucket,
            f"{folder}/{object_name}")
        # https://stackoverflow.com/questions/52336902/what-is-the-difference-between-s3-client-upload-file-and-s3-client-upload-file

    except ClientError as e :
        print(f'Credential error => {e}')
    except Exception as e :
        print(f"Another error => {e}")


s3 = s3_connection()