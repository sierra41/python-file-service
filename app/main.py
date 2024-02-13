from dataclasses import asdict

import uvicorn
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.database.database import db
from app.core.config import conf
from app.errors import handler
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from app.api.main import api_router

# main.py - fastapi 실행
## main.py 파일에 생성한 app 객체 : FastAPI의 핵심 객체
## app 객체를 통해 FastAPI의 설정
## 프로젝트의 전체적인 환경을 설정



def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    ## 데이터베이스 이니셜라이즈

    ## 레디스 이니셜라이즈

    ## 미들웨어 정의
    # 가장 밑에 있는 미들웨어부터 실행
    #app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        # 특정 도메인에서 특정 호스트로만 접속 가능하도록 정의하는 미들웨어.
        # 해당 미들웨어가 없으면 백엔드의 도메인과 프론트엔드의 도메인이 같아야만 응답을 주고 받을 수 있다.
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])

    ## 라우터 정의
    app.include_router(api_router)
    handler.include_app(app)


    return app


app = create_app()

if __name__ == "__main__":
    #logger.info("----------__main__ start----------");
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
