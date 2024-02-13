from typing import List

from fastapi import Form
from pydantic.main import BaseModel

from app.api.models.enums import ProjectType, AccessType, QualityType


class FileDownloadRequest(BaseModel):
    access_type: List[AccessType]
    file_id: int

    class Config:
        use_enum_values = True
        orm_mode = True



class OthersFileUploadRequest(BaseModel):
    project_type: List[ProjectType]
    access_type: List[AccessType]
    user_info: str

    @classmethod
    def as_form(cls, project_type: List[ProjectType] = Form(...), access_type: List[AccessType] = Form(...),
                user_info: str = Form(...)) -> 'OthersFileUploadRequest':
        return cls(project_type=project_type, access_type=access_type, user_info=user_info)

    class Config:
        use_enum_values = True
        orm_mode = True


class ImagesFileUploadRequest(BaseModel):
    project_type: List[ProjectType]
    access_type: List[AccessType]
    quality_type: List[QualityType]
    user_info: str
    resize_width: int = 300
    resize_height: int = None

    @classmethod
    def as_form(cls, project_type: List[ProjectType] = Form(...), access_type: List[AccessType] = Form(...), quality_type: List[QualityType] = Form(...),
                user_info: str = Form(...), resize_width: int = Form(...) == None, resize_height: int = Form(...) == None ) -> 'ImagesFileUploadRequest':
        return cls(project_type=project_type, access_type=access_type, quality_type=quality_type, user_info=user_info, resize_width=resize_width, resize_height=resize_height)

    class Config:
        use_enum_values = True
        orm_mode = True


