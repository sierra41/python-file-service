class StatusCode():
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    NotFoundFile = 400


class NotFoundFile(Exception):
    print("NotFoundFile Error")

    def __init__(self,
                 code: str = None,
                 msg: str = None,
                 detail: str = None
                 ):
        self.msg = f"업로드 파일을 찾을 수 없습니다."
        self.detail = f"Not Found File"
        self.code = f"FILE-UPLOAD-0"
        self.ex = Exception

    pass


class ExceededFileSize(Exception):
    print("ExceededFileSize Error")

    def __init__(self,
                 code: str = None,
                 msg: str = None,
                 detail: str = None
                 ):
        self.msg = f"허용 가능한 파일 크기를 초과했습니다."
        self.code = f"FILE-UPLOAD-6"
        self.detail = f"Exceeded File Size"
        self.ex = Exception

    pass



class NotAllowedFileType(Exception):
    print("ExceededFileSize Error")

    def __init__(self,
                 code: str = None,
                 msg: str = None,
                 detail: str = None
                 ):

        self.msg = f"허용되지 않은 타입의 파일입니다."
        self.code = f"FILE-UPLOAD-1"
        self.detail = f"FILE_TYPE_IS_NOT_ALLOWED"
        self.ex = Exception

    pass
