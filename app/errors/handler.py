import sqlalchemy
from fastapi import status, HTTPException, Request, Response
from starlette.responses import JSONResponse

from app.errors.errors import *




def bad_request_exception_handler(request: Request, exc: Exception):
    print("bad_request_exception_handler")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"success": "false", "msg": f"{exc.msg}", "code": f"{exc.code}", "detail": f"{exc.detail}"}
                        )


def not_found_exception_handler(request: Request, exc: Exception):
    print("not_found_exception_handler")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={"success": "false", "msg": f"{exc.msg}", "code": f"{exc.code}", "detail": f"{exc.detail}"}
                        )


def include_app(app):
    app.add_exception_handler(NotFoundFile, bad_request_exception_handler)
    app.add_exception_handler(ExceededFileSize, bad_request_exception_handler)
    app.add_exception_handler(NotAllowedFileType, bad_request_exception_handler)
