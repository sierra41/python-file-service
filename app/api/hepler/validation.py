from typing_extensions import IO

from app.api.hepler.createFileValue import get_file_size
from app.api.models.enums import FilesType
from app.core.consts import MAX_OTHERS_FILE_SIZE, MAX_VIDEO_FILE_SIZE, MAX_IMAGE_FILE_SIZE
from app.errors.errors import *


#파일 분리
async def check_validation_file(fileObj, requestType):
    print("check_validation_file. requestType :", requestType)
    await check_file_empty(fileObj=fileObj)
    if requestType == FilesType.others:
        await check_file_type(currentType= fileObj.content_type, requestType=requestType)
        size = await check_other_file_size(fileObj=fileObj, MaxSize=MAX_OTHERS_FILE_SIZE)
    if requestType == FilesType.videos:
        await check_file_type(currentType= fileObj.content_type, requestType=requestType)
        size = await check_file_size(fileObj=fileObj, MaxSize=MAX_VIDEO_FILE_SIZE)
    if requestType == FilesType.images:
        await check_file_type(currentType=fileObj.content_type, requestType=requestType)
        size = await check_file_size(fileObj=fileObj, MaxSize=MAX_IMAGE_FILE_SIZE)
    print("check_validation_file. size :", size)
    return size





async def check_file_empty(fileObj: IO):
    print("check_file_empty.")
    if not fileObj:
        raise NotFoundFile()


async def check_file_type(currentType, requestType):
    print("check_file_type. currentType : ", currentType, ", requestType : ",requestType )
    if currentType not in requestType:
        raise NotAllowedFileType()

async def check_file_image_type(currentType):
    return ["GIF",".gif"] if currentType == 'image/gif' else ["JPEG",".jpg"]


async def check_other_file_size(fileObj: IO, MaxSize):
    print("check_file_size. MaxSize:",MaxSize)
    real_file_size = await get_file_size(fileObj)
    #real_file_size = fileObj.file.tell()
    if  real_file_size > MaxSize:
        raise ExceededFileSize()
    return real_file_size

async def check_file_size(fileObj: IO, MaxSize):
    print("check_file_size. MaxSize:",MaxSize)
    #real_file_size = await get_file_size(fileObj)
    real_file_size = fileObj.file.tell()
    if  real_file_size > MaxSize:
        raise ExceededFileSize()
    return real_file_size


async def check_file2_size(file: IO, MaxSize):
    print("check_file2_size. MaxSize:",MaxSize)
    real_file_size = len(file)

    file.seek(0)
    return real_file_size
