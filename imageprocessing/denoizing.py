import numpy as np
import cv2 as cv
from skimage.io import imsave
import sys


class DenoizeModel:
    def __init__(self, local_dir="data/"):
        self.local_dir = local_dir

    def denoizing(self, img_name):
        img = cv.imread(self.local_dir + img_name)

        dst = cv.fastNlMeansDenoisingColored(src=img, dst=None, h=5, hColor=7,
                                             templateWindowSize=7, searchWindowSize=21)
        denoize_name = self.get_denoize_name_(img_name)
        imsave(self.local_dir + denoize_name, dst)

        return denoize_name

    def get_denoize_name_(self, img_name):
        name = str(img_name).split(".")
        return name[0] + "_denoize." + name[1]


if __name__ == '__main__':
    # сюда нужно передать путь до папки, в которой будут лежать фотографии
    denoize_model = DenoizeModel(local_dir="data/")

    img_name = sys.argv[1]
    # получает на вход имя файла в папке, сохраняет в ту же папку фото без шума и возвращает его имя
    denoize_img_name = denoize_model.denoizing(img_name)

    print(denoize_img_name)
