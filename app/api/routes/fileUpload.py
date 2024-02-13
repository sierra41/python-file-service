import tempfile

from fastapi import APIRouter, Depends, UploadFile, File

from app.api.dto.create import create_video_file, create_images_file, create_resized_images_file, create_others_file, \
    create_ready_images_file
from app.api.hepler.convert import convert_image
# import os
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/Users/personal/company/file-service/venv/lib/python3.9/site-packages/ffmpeg"
# import subprocess
# from moviepy.editor import VideoFileClip


from app.api.hepler.createFileValue import check_bucket_name, get_file_size
from app.api.hepler.resize import resize_image
from app.api.hepler.validation import check_validation_file, check_file_image_type
from app.api.models.enums import FilesType, Status
from app.api.models.models import FileSizeInfo
from app.api.models.request import OthersFileUploadRequest, ImagesFileUploadRequest
from app.database.schema import Files
from app.utils.s3.s3 import s3_connection, upload_file
from sqlalchemy.orm import Session
from app.database.database import db

router = APIRouter(prefix="/uploads")


# Description : 일반파일 업로드


@router.post("/others", status_code=200)
async def upload_others_file(othersFileRequest: OthersFileUploadRequest = Depends(OthersFileUploadRequest.as_form),
                             file_obj: UploadFile = File(...), session: Session = Depends(db.session)):
    print("upload_others_file - othersFileRequest : ", othersFileRequest, "file : ", file_obj, ", filename : ", file_obj.filename,
          ", content_type : ", file_obj.content_type)
    bucket_name = check_bucket_name(othersFileRequest.access_type)
    size = await check_validation_file(fileObj=file_obj, requestType=FilesType.others)
    new_file = await create_others_file(session, othersFileRequest, file_obj, bucket_name, size)
    await save_s3_file(file=file_obj.file, newFile=new_file, bucketName=bucket_name)
    update_new_file = Files.filter(session=session, id=new_file.id)
    update_new_file.update(auto_commit=True, **{"status": Status.UPLOAD_SUCCESS})


    # upload_file = io.BytesIO()
    # while True:
    #     chunk = await file_obj.read(1024)
    #     if not chunk:
    #         break
    #     upload_file.write(chunk)
    return {"filename": file_obj.filename}


# Description : 동영상 업로드
@router.post("/video", status_code=200)
async def upload_video_file(othersFileInfo: OthersFileUploadRequest = Depends(OthersFileUploadRequest.as_form),
                            file_obj: UploadFile = File(...), session: Session = Depends(db.session)):
    print("upload_video_file - uploadFileInfo : ", othersFileInfo, "file : ", file_obj, ", filename : ", file_obj.filename,
          ", content_type : ", file_obj.content_type)

    size = await check_validation_file(fileObj=file_obj, requestType=FilesType.videos)
    # thumbnail db save
    # thumbnail create
    # thumbnail s3 save

    # video convert
    # video db save
    # video s3 save
    #video_input_path = '/your/video.mp4'
    #img_output_path = '/your/image.jpg'
    #subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])
    # 저장할 경로 + 파일명

    path = "/Users/Downloads/"
    # test_filename = os.path.join(path, file_obj.filename)
    # with open(test_filename, "wb+") as file_object:
    #     shutil.copyfileobj(file_obj.file, file_object)
    # async with aiofiles.open(file_obj.filename, 'wb') as out_file:
    #     content = await file_obj.read()  # async read
    #     await out_file.write(content)
    local_file = tempfile.NamedTemporaryFile()
    local_file.write(file_obj.file.read())
    #local_file.wri

    print("path.11111111")
    #local_file.write(path   +file_obj.filename)
    #files = os.listdir(path)

    print("local_file.11111111")
    # clip = VideoFileClip(path+local_file.name)
    #
    # print("clip.11111111")
    # print("clip. :", clip)
    # thumbnail = clip.save_frame(file_obj.filename+ ".jpg", t=1)
    # print("thumbnail.11111111")
    # print("thumbnail. :", thumbnail)
    # convert_video = clip.write_videofile(file_obj.filename+".mp4")
    # print("convert_video.11111111")
    # print("convert_video. :", convert_video)
    bucket_name = check_bucket_name(othersFileInfo.access_type)

    new_file = await create_video_file(session, othersFileInfo, file_obj, bucket_name, size)
    #new_file = await save_db_video_file(session, othersFileInfo, file_obj, bucket_name, size)
    await save_s3_file(file=file_obj.file, newFile=new_file, bucketName=bucket_name)


    return {"filename": file_obj.filename}





# Description : 이미지 업로드
@router.post("/images", status_code=200)
async def upload_images_file(imagesFileRequest: ImagesFileUploadRequest = Depends(ImagesFileUploadRequest.as_form),
                             file_objs: list[UploadFile] = File(...), session: Session = Depends(db.session)):
    print("upload_images_file - imagesFileRequest : ", imagesFileRequest, "file_objs count : ", len(file_objs))


    bucket_name = check_bucket_name(imagesFileRequest.access_type)
    for file_obj in file_objs:
        # size, extension
        size = await check_validation_file(fileObj=file_obj, requestType=FilesType.images)
        extension = await check_file_image_type(file_obj.content_type)
        new_file, new_refile = await create_ready_images_file(session, imagesFileRequest, file_obj, bucket_name, size=size, extension=extension[1])


        # original convert, original db save, original s3 save
        buf, converted_img, converted_size = await convert_image(file_obj=file_obj, extension=extension[0], quality_type=imagesFileRequest.quality_type)
        update_new_file = Files.filter(session=session, id=new_file.id)
        update_new_file.update(auto_commit=True, **{"width": converted_img.size[0], "height": converted_img.size[1], "status": Status.CONVERT_SUCCESS, "size": converted_size})
        await save_s3_file(file=buf, newFile=new_file, bucketName=bucket_name)
        update_new_file.update(auto_commit=True, **{"status": Status.UPLOAD_SUCCESS})


        # resizing, resizied db save, resizied s3 save
        buf, resized_img, resized_size = await resize_image(converted_img=converted_img, extension=extension[0], resize_width=imagesFileRequest.resize_width, resize_height=imagesFileRequest.resize_height)
        update_new_refile = Files.filter(session=session, id=new_refile.id)
        update_new_refile.update(auto_commit=True, **{"width": resized_img.size[0], "height": resized_img.size[1], "status": Status.RESIZE_SUCCESS, "size": resized_size})
        await save_s3_file(file=buf, newFile=new_refile, bucketName=bucket_name)
        update_new_refile.update(auto_commit=True, **{"status": Status.UPLOAD_SUCCESS})
        buf.close()
        file_obj.file.close()

    return {"filename": [file_obj.filename for file_obj in file_objs]}





async def save_s3_file(file, newFile, bucketName):
    s3_client = s3_connection()

    upload_file(s3_client,
                 file=file,
                 bucket=bucketName,
                 folder=newFile.path,  # To Be updated
                 object_name=newFile.key)



