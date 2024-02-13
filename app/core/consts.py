# consts.py
## 환경에도 변하지 않는 상수들 정의
import os

WEBSITE_ADDR = "youtube.com"


# "/" : main. healthcheck용, "/openapi.json": /docs /redoc 에서 api만들 때 사용하는 파일
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
# /docs /redoc : 스웨거 등 문서 /auth : 로그인, 회원가입 등 인증
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"

PROFILE = "local"


MAX_OTHERS_FILE_SIZE = 2000000000
MAX_VIDEO_FILE_SIZE = 500000000
MAX_IMAGE_FILE_SIZE = 200000000


#BASE_DIR = os.getcwd()
#IMAGE_DIR = os.path.join(BASE_DIR, 'images')
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_DEFAULT_REGION = "ap-northeast-2"
AWS_PUBLIC_BUCKET_NAME = "efile-public-s3-local"
AWS_PRIVATE_BUCKET_NAME = "efile-public-s3-local"
AWS_MULTIPART_MIN_PART_MB = 8
