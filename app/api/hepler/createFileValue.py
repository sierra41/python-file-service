import uuid
from typing import IO
from uuid import uuid4

from app.core.consts import PROFILE, AWS_DEFAULT_REGION, AWS_PRIVATE_BUCKET_NAME, AWS_PUBLIC_BUCKET_NAME
import urllib.parse

async def get_file_size(fileObj: IO):
    #fileObj.file.seek(0, 2)
    real_file_size = 0
    for chunk in fileObj.file:
        real_file_size += len(chunk)
    await fileObj.seek(0)
    print("real_file_size. real_file_size :", real_file_size)
    return real_file_size


async def generate_unique_key():
    uniqueKey = uuid.uuid1()
    print("generate_unique_key. uniqueKey :", uniqueKey)
    return str(uniqueKey)


# 환경 추가
async def generate_path(projecType, key):
    path = PROFILE + "/" + projecType + "/" + str(key)
    print("generate_path. path :", path)
    return path


async def generate_url(path, bucket_name, key):
    url_parts = list(urllib.parse.urlparse(get_base_url(bucket_name)))
    url_parts[2] = path + "/" + key
    # url_parts[4] = urllib.parse.urlencode(args_dict)
    url = urllib.parse.urlunparse(url_parts)
    print("generate_url. url :", url)
    return url


def get_base_url(bucket_name):
    return "https://" + bucket_name + ".s3." + AWS_DEFAULT_REGION + ".amazonaws.com/"


def check_bucket_name(access_type: str):
    bucket_name = None

    if access_type == "private":
        bucket_name = AWS_PRIVATE_BUCKET_NAME
        # return get_email 로그인한 이메일값의 사용이 필요하면 이런식으로도 사용 가능
    bucket_name = AWS_PUBLIC_BUCKET_NAME
    print("bucket_name", bucket_name)
    return bucket_name