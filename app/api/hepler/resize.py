from io import BytesIO

from PIL import Image, ImageSequence



async def resize_width_hight(or_width, or_hight, re_width, re_hight):
    print("re_width :", re_width, "re_hight :", re_hight)
    resize_w = re_width if re_width != 0 else 300
    resize_h = re_hight if re_hight != 0 else int(
        or_hight * (resize_w / (or_width)))
    print("resize_h. :", resize_h, "resize_w. :", resize_w)
    return resize_w, resize_h



async def resize_image(converted_img, extension, resize_width, resize_height):
    resize_w, resize_h = await resize_width_hight(or_width=converted_img.size[0], or_hight=converted_img.size[1],
                                                  re_width=resize_width,
                                                  re_hight=resize_height)
    if extension != "GIF":
        resized_img = converted_img.resize((resize_w, resize_h), Image.LANCZOS)
        buf = BytesIO()
        resized_img.save(buf, extension, quality=95)
    else:
        frames = ImageSequence.Iterator(converted_img)
        frames = thumbnails(frames, resize_w, resize_h)

        resized_img = next(frames)
        resized_img.info = converted_img.info
        buf = BytesIO()


        resized_img.save(buf, extension, save_all=True, append_images=list(frames), loop=0, quality=95)
    resized_size =  buf.tell()
    print("[resize_image] resized_size :", resized_size)

    buf.seek(0)
    return buf, resized_img, resized_size



def thumbnails(frames, resize_w, resize_h):
    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail((resize_w, resize_h), Image.LANCZOS)
        yield thumbnail