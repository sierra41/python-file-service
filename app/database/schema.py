from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum, Boolean, Double,

)
from sqlalchemy.orm import Session, relationship
from app.database.database import Base, db


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, nullable=False, default=func.localtimestamp())

    # updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "create_date"]

    def __hash__(self):
        return hash(self.id)
    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, **kwargs):
        """
        Simply get a Row
        :param kwargs:
        :return:
        """
        session = next(db.session())
        # 회원가입(create)의 경우는 commit=ture가 필요하기 때문에 받은 session으로 작업하는데 로그인은 commit 과정이 필요없기 때문에 또 다른 session을 받아와서 사용 가능. 리턴 후 자동반납
        # 따라서 함수 한개가 작동할 때 session이 동시에 여러개 열릴 수 있음.
        # 나중에 트래픽이나 다른 부분이 부담이 된다면 회원가입처럼 session을 받아서 사용가능.
        query = session.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one row.")
        # 나중에 filter 추가
        return query.first()

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 1:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt': cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte': cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt': cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte': cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in': cond.append((col.in_(val)))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls


    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        get_id = self.id
        ret = None

        self._session.flush()
        if qs > 0 :
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    # def update(self, _session: Session = None, auto_commit: bool = False, **kwargs):
    #     cls = self.cls_attr()
    #     if _session:
    #         query = _session.query(cls)
    #     else:
    #         _session = next(db.session())
    #         query = _session.query(cls)
    #     self.close()
    #     return query.update(**kwargs)
    #





    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        print(self.served)
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


# Enum 정리
class Files(Base, BaseMixin):
    __tablename__ = "tb_file"
    access_type = Column(Enum("PRIVATE", "PUBLIC"), default="public")
    project_type = Column(Enum("WINGCHAT", "PROPOINT", "TECHSIGN"), default="public")
    active = Column(Boolean, nullable=True, default=True)
    key = Column(String(length=100), nullable=True, unique=True)
    path = Column(String(length=255), nullable=True)
    url = Column(String(length=255), nullable=True)
    original_name = Column(String(length=255), nullable=True)
    status = Column(Enum("READY", "SAVE_SUCCESS", "CONVERT_SUCCESS", "RESIZE_SUCCESS", "UPLOAD_SUCCESS", "FAIL"),
                    default="public")
    type = Column(String(length=100), nullable=True)
    size = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    video_second = Column(Double, nullable=True)
    parent_id = Column(Integer, nullable=True)
    #partent_id = relationship("Files", back_populates="tb_file")

#
#
# class Users(Base, BaseMixin):
#     __tablename__ = "users"
#     status = Column(Enum("active", "deleted", "blocked"), default="active") # Enum 정의된 내용중 하나가 아니면 에러
#     email = Column(String(length=255), nullable=True)
#     pw = Column(String(length=2000), nullable=True)
#     name = Column(String(length=255), nullable=True)
#     phone_number = Column(String(length=20), nullable=True, unique=True)
#     profile_img = Column(String(length=1000), nullable=True)
#     sns_type = Column(Enum("FB", "G", "K"), nullable=True) #소셜 로그인
#     marketing_agree = Column(Boolean, nullable=True, default=True)
