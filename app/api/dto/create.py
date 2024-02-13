from app.api.hepler.createFileValue import generate_path, generate_unique_key, generate_url
from app.api.models.enums import Status
from app.database.schema import Files





async def create_others_file(session, othersFileInfo, file_obj, bucket_name, size):

    key = await generate_unique_key()
    path = await generate_path(othersFileInfo.project_type[0], key)
    url = await generate_url(path, bucket_name, key)
    new_file = Files.create(session, auto_commit=True,
                            access_type=othersFileInfo.access_type[0],
                            key=key,
                            path=path,
                            url=url,
                            project_type=othersFileInfo.project_type[0],
                            original_name=file_obj.filename,
                            status=Status.READY,
                            type=file_obj.content_type,
                            size=size)
    return new_file


async def create_video_file(session, othersFileInfo, file_obj, bucket_name, size):

    key = await generate_unique_key()
    path = await generate_path(othersFileInfo.project_type[0], key)
    url = await generate_url(path, bucket_name, key)
    new_file = Files.create(session, auto_commit=True,
                            access_type=othersFileInfo.access_type[0],
                            key=key,
                            path=path,
                            url=url,
                            project_type=othersFileInfo.project_type[0],
                            original_name=file_obj.filename,
                            status=Status.READY,
                            type=file_obj.content_type,
                            size=size)
    return new_file



async def create_ready_images_file(session, imagesFileInfo, file_obj, bucket_name, size, extension):

    key = await generate_unique_key() + extension
    path = await generate_path(imagesFileInfo.project_type[0], key)
    url = await generate_url(path, bucket_name, key)

    new_file = Files.create(session, auto_commit=True,
                            access_type=imagesFileInfo.access_type[0],
                            key=key,
                            path=path,
                            url=url,
                            project_type=imagesFileInfo.project_type[0],
                            original_name=file_obj.filename,
                            status=Status.READY,
                            type=file_obj.content_type,
                            size=size,
                            )


    re_key = key + extension
    re_url = url + extension
    new_refile = Files.create(session, auto_commit=True,
                            access_type=imagesFileInfo.access_type[0],
                            key=re_key,
                            path=path,
                            url=re_url,
                            project_type=imagesFileInfo.project_type[0],
                            original_name=file_obj.filename,
                            status=Status.READY,
                            type=file_obj.content_type,
                            parent_id=new_file.id
                            )
    return new_file, new_refile




async def create_images_file(session, imagesFileInfo, file_obj, bucket_name, img_size, size, extension):

    key = await generate_unique_key() + extension
    path = await generate_path(imagesFileInfo.project_type[0], key)
    url = await generate_url(path, bucket_name, key)

    saved_file = Files.create(session, auto_commit=True,
                            access_type=imagesFileInfo.access_type[0],
                            key=key,
                            path=path,
                            url=url,
                            project_type=imagesFileInfo.project_type[0],
                            original_name=file_obj.filename,
                            status=Status.READY,
                            type=file_obj.content_type,
                            size=size,
                            width=img_size[0],
                            height=img_size[1]
                            )

    return saved_file


async def create_resized_images_file(session, new_file, img_size, extension):
    key = new_file.key + extension
    url = new_file.url + extension
    saved_file = Files.create(session, auto_commit=True,
                            access_type=new_file.access_type,
                            key=key,
                            path=new_file.path,
                            url=url,
                            project_type=new_file.project_type,
                            original_name=new_file.original_name,
                            status=Status.READY,
                            type=new_file.type,
                            size=new_file.size,
                            width=img_size[0],
                            height=img_size[1],
                            parent_id=new_file.id
                            )
    return saved_file


