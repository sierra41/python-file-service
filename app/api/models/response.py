from datetime import datetime
from typing import List

from pydantic.main import BaseModel

from app.api.models.enums import ProjectType, AccessType, QualityType




class FileInfoResponse(BaseModel):
    id: int
    #pw: str = None
    originName: str = None
    contentType: str = None
    status: str = None
    size: int = None
    width: int = None
    height: int = None
    accessType: List[AccessType] = None
    #processType: List[ProjectType] = None
    video_second: float = None
    url: str = None
    createDate: datetime = None
    child: str = None
    parent: str = None

    class Config:
        orm_mode = True


class CoFileResponse(BaseModel):
    id: int
    originName: str = None
    contentType: str = None
    status: str = None
    size: int = None
    width: int = None
    height: int = None
    accessType: List[AccessType] = None
    #processType: List[ProjectType] = None
    video_second: float = None
    url: str = None
    createDate: datetime = None
    child: str = None
    parent: str = None