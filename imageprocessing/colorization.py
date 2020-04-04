import Algorithmia
import sys

class AlgoClient():
    def __init__(self, local_dir="data/"):
        self.local_dir = local_dir

        #hardcode настроек сайта
        self.model_name = 'deeplearning/ColorfulImageColorization/1.1.13'
        self.cloud_in_dir = "data://.my/data_in/"
        self.apiKey = 'simIVvEvW9njMmOIYwAtYFdxtFe1'

        self.client = Algorithmia.client(self.apiKey)
        self.algo = self.client.algo(self.model_name)

    def colorize(self, img_name):
        #загрузка файла на сайт
        self.client.file(self.cloud_in_dir + img_name).putFile(self.local_dir + img_name)

        #раскраска
        input = {"image": self.cloud_in_dir + img_name}
        cloud_color_img = self.algo.pipe(input).result['output']

        #загрузка файла с сайта
        color_file = self.client.file(cloud_color_img).getBytes()

        #запись в файл
        color_img_name = self.get_color_name_(cloud_color_img)
        with open(self.local_dir + color_img_name, "wb") as f:
            f.write(color_file)

        return color_img_name

    def get_color_name_(self, img_url):
        name = str(img_url).split('/')[-1].split(".")
        return name[0] + "_color." + name[1]


if __name__ == '__main__':
    # сюда нужно передать путь до папки, в которой будут лежать фотографии
    algoclient = AlgoClient(local_dir="data/")

    img_name = sys.argv[1]
    # получает на вход имя файла в папке
    color_img_path = algoclient.colorize(img_name)

    print(color_img_path)