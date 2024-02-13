from dataclasses import dataclass
from os import environ, path

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
# 현재 파일 기준으로 파일 프로젝트 폴더 위치 설정


# config.py
## 환경에 따른 서버별 변수
# dictionary 형식으로 가지고 오고 싶을 경우에 @dataclass 사용

@dataclass
class Config:
  """
  기본 Configuration -
  """
  BASE_DIR = base_dir

  DB_POOL_RECYCLE: int = 900
  DB_ECHO: bool = True
  #사용되는 sql 프린트해주는 옵션


@dataclass
class LocalConfig(Config):
  """
  Local Configuration
  """
  #PROJ_RELOAD: bool = True
  # PROJ_RELOAD: bool = True
  DB_USERNAME = ""
  DB_PASSWORD = ""
  DB_HOST = ""
  DB_PORT = "3306"
  DB_DATABASE = "file-service"

  DB_URL: str = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
  #DB_URL: str = "mysql+pymysql://"
    #데이터베이스 연동 : mysql+pymysql://${USERNAME}:${PASSWORD}@${HOST}:{PORT}/${DATABASE}?charset=utf8mb4$
  #logger.info("----------[config] DB_URI----------", DB_URL)
  TRUSTED_HOSTS =["*"]
  ALLOW_SITE =["*"]

@dataclass
class ProdConfig(Config):
  """
  Prod Configuration -
  """
  #PROJ_RELOAD: bool = False
  TRUSTED_HOSTS =["*"]
  ALLOW_SITE =["*"]

#print(asdict(LocalConfig())) # 클래스가 dict 로 변경됨

# def abc(DB_ECHO=None, DB_POOL_RECYCLE=None, **kwargs):
#     print(DB_ECHO, DB_POOL_RECYCLE)
# arg = asdict(LocalConfig())  # unpacking
# abc(**arg) - 각각 값으로 가져옴

def conf():
  """
  환경 불러오기
  :return:
  """
  config = dict(prod=ProdConfig(), local=LocalConfig())
  return config.get(environ.get("API_ENV", "local"))
# API_ENV가 없으면 local 사용하라는 의미
## 파이썬에서는 switch case 가 없어서 이렇게 사용

