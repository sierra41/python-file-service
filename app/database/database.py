from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging


# db 연결, session관리
class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        #logger.info("----------[conn] init_app----------");

        database_url = kwargs.get("DB_URL")
        #print("database_url", database_url)
        #logger.info("----------[conn] DB database_url----------", database_url)
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)

        self._engine = create_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        @app.on_event("startup")  # 앱 실행시
        def startup():
            self._engine.connect()
            logging.info("DB connected.")

        @app.on_event("shutdown") # 앱 종료시
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB disconnected")

    # sess
    def get_db(self):
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session # db 연결 성공 후 db 세션시작
        finally:
            db_session.close() # api 호출이 끝나면 세션 종료

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()
