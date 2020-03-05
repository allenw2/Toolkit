import os

from removebg import RemoveBg
from PIL import Image

rmbg = RemoveBg('ro3n6EvmiWGi3QNhy59tsbfd', 'error.log')
dir_ = os.path.join('C:\\', 'Users', 'Allen', 'Desktop', 'pic')


def get_id_photo(path, color):
    for pic in os.listdir(path):
        rmbg.remove_background_from_img_file(os.path.join(path, pic))

    for pic in os.listdir(path):
        pic_path = os.path.join(path, pic)
        if 'no_bg' in pic:
            no_bg = Image.open(pic_path)
            x, y = no_bg.size
            new_pic = Image.new('RGBA', no_bg.size, color=color)
            new_pic.paste(no_bg, (0, 0, x, y), no_bg)
            new_pic.save(os.path.join(path, 'new_' + str(pic).rsplit('.', 1)[0] + '.png'))
            os.remove(pic_path)


if __name__ == '__main__':
    get_id_photo(dir_, 'white')
