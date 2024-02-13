from io import BytesIO

from PIL import Image
from pillow_heif import register_heif_opener

from app.api.models.enums import QualityType


def get_quality(quality_type):
    print("quality_type :", quality_type)
    if quality_type == QualityType.LOW:
       return 10
    if quality_type == QualityType.STANDARD:
       return 40
    if quality_type == QualityType.ORIGINAL:
       return 95

async def convert_image(file_obj, extension, quality_type):
    register_heif_opener()

    converted_img = Image.open(file_obj.file)
    quality = get_quality(quality_type[0])
    print("[convert_image] quality :", quality)
    buf = BytesIO()
    if file_obj.content_type != 'image/gif':
        print("[convert_image] content_type :", file_obj.content_type)
        if converted_img.mode in ("RGBA", "P"):
            converted_img = converted_img.convert("RGB")
        converted_img.save(buf, extension, quality=quality)
    else:
        converted_img.save(buf, extension, save_all=True, loop=0, quality=quality)
    converted_size =  buf.tell()
    print("[convert_image] converted_size :", converted_size)

    buf.seek(0)
    return buf, converted_img, converted_size

