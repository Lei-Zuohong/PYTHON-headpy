# -*- coding: UTF-8 -*-
# Public package
# Private package
import PIL.Image as Image


def pics_to_pdf(path_pics=[],
                path_pdf=''):
    pic_list = []
    for count, path_pic in enumerate(path_pics):
        pic = Image.open(path_pic)
        if(pic.mode == 'RGBA'):
            pic.convert('RGB')
        if(count == 0):
            pic_out = pic
        else:
            pic_list.append(pic)
    pic_out.save(path_pdf, 'PDF', resolution=100.0, save_all=True, append_images=pic_list)
    return 1

