from enum import Enum
from typing import Dict, Any

from fastapi import HTTPException
from starlette.responses import JSONResponse


class StatusCode(int, Enum):
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    NotFoundFile = 400


class APIException:
    pass


# @staticmethod
# async def exception_handler(error: APIException):
#     error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
#     res = JSONResponse(status_code=error.status_code, content=error_dict)
#     return res

class CustomException:
    pass


class BaseHttpException(Exception):
    status_code: int = None
    detail: str = None
    headers: Dict[str, Any] = None
    def __init__(self):
        super().__init__(CustomException
            # status_code=self.status_code,
            # detail=self.detail,
            # headers=self.headers
        )


class CustomException(BaseHttpException):
    status_code = StatusCode.HTTP_400
    detail = f"업로드 파일을 찾을 수 없습니다."
    #headers = f"Not Found File "
   # headers = "code": f"FILE-UPLOAD-0"

# status_code = StatusCode.HTTP_400,
# msg = f"업로드 파일을 찾을 수 없습니다.",
# detail = f"Not Found File ",
# code = f"FILE-UPLOAD-0",
# ex = ex,

class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
            self,
            *,
            status_code: int = StatusCode.HTTP_500,
            code: str = "000000",
            msg: str = None,
            detail: str = None,
            ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


# class NotFoundFile(APIException):
#     print("NotFoundFile1111111111111111111111 : ", APIException)
#     def __init__(self, ex: Exception = None):
#          super().__init__(
#              status_code=StatusCode.HTTP_400,
#              msg=f"업로드 파일을 찾을 수 없습니다.",
#              detail=f"Not Found File ",
#              code=f"FILE-UPLOAD-0",
#              ex=ex,
#          )


class ExceededFileSize(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"허용 가능한 파일 크기를 초과했습니다.",
            detail=f"Exceeded File Size : {user_id}",
            code=f"FILE-UPLOAD-6",
            ex=ex,
        )


class NotFoundUserEx(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"해당 유저를 찾을 수 없습니다.",
            detail=f"Not Found User ID : {user_id}",
            code=f"{StatusCode.HTTP_400}{'1'.zfill(4)}",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"비정상적인 접근입니다.",
            detail="Token has been compromised.",
            code=f"{StatusCode.HTTP_400}{'2'.zfill(4)}",
            ex=ex,
        )
