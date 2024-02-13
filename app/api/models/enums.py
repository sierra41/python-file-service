

from enum import Enum
from typing import List




class ProjectType(str, Enum):
    WINGCHAT: str = "WINGCHAT"
    PROPOINT: str = "PROPOINT"
    TECHSIGN: str = "TECHSIGN"


class AccessType(str, Enum):
    PRIVATE: str = "PRIVATE"
    PUBLIC: str = "PUBLIC"

class QualityType(str, Enum):
    LOW: str = "LOW"
    STANDARD: str = "STANDARD"
    ORIGINAL: str = "ORIGINAL"




class FilesType(str, Enum):
    others: List[str] = ["audio/mp4",
                         "audio/ogg",
                         "audio/webm",
                         "application/vnd.ms-excel",
                         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         "application/zip",
                         "application/pdf",
                         "text/plain",
                         "text/csv",
                         "image/svg+xml"]
    images: List[str] = ["image/png",
                         "image/jpg",
                         "image/jpeg",
                         "image/bmp",
                         "image/gif",
                         "image/ief",
                         "image/pipeg",
                         "image/tiff",
                         "image/heic"]
    videos: List[str] = ["video/quicktime",
                         "video/mp4",
                         "video/ogg",
                         "video/webm",
                         "video/mpeg",
                         "video/mov",
                         "application/octet-stream"]


class Status(str, Enum):
    READY: str = "READY"
    SAVE_SUCCESS: str = "SAVE_SUCCESS"
    CONVERT_SUCCESS: str = "CONVERT_SUCCESS"
    RESIZE_SUCCESS: str = "RESIZE_SUCCESS"
    UPLOAD_SUCCESS: str = "UPLOAD_SUCCESS"
    FAIL: str = "FAIL"


