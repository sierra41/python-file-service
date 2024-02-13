from pydantic.main import BaseModel


class Token(BaseModel):
    Authorization: str = None
    # response model

class FileS3Info(BaseModel):
    url: str = None
    # response model
    class Config:
        orm_mode = True



class FileSizeInfo(BaseModel):
    width: int = None
    height: int = None
    # response model
    class Config:
        orm_mode = True
