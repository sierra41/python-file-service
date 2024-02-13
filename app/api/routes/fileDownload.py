from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.api.hepler.createFileValue import check_bucket_name
from app.api.models.request import FileDownloadRequest
from sqlalchemy.orm import Session
from app.database.database import db
from app.database.schema import Files
from app.utils.s3.s3 import download_file, s3_connection

router = APIRouter(prefix="/downloads")




@router.post("/others", status_code=200)
async def upload_others_file(fileDownloadRequest: FileDownloadRequest,
                             session: Session = Depends(db.session)):
    print("upload_others_file - FileDownloadRequest : ", FileDownloadRequest)

    #
    # bucket_name = check_bucket_name(uploadFileInfo.access_type)
    # size = await check_validation_file(fileObj=file_obj, requestType=FilesType.others)
    # new_file = await create_others_file(session, uploadFileInfo, file_obj, bucket_name, size)
    # await save_s3_file(file=file_obj.file, newFile=new_file, bucketName=bucket_name)
    # update_new_file = Files.filter(session=session, id=new_file.id)
    # update_new_file.update(auto_commit=True, **{"status": Status.UPLOAD_SUCCESS})
    bucket_name = check_bucket_name(fileDownloadRequest.access_type)
    file = Files.filter(session=session, id=fileDownloadRequest.file_id)
    contents = await download_s3_file(key=file.key, bucketName=bucket_name)

    #headers = {'Content-Disposition': f'attachment; filename="{file.original_name}"'}
    headers = {
        'Content-Disposition': f'attachment;filename={file.original_name}',
        'Content-Type': 'application/octet-stream',
    }
    #return Response(contents, headers=headers, media_type='audio/mp3')
    return FileResponse(content=contents, path=file.url, headers=headers, filename=file.original_name, media_type=file.type)




async def download_s3_file(bucketName, key):
    s3_client = s3_connection()

    content = download_file(s3_client,
                 bucketName=bucketName,
                 key=key)
    return content