import Algorithmia
import sys

def get_color_name(url):
    name = url.split('/')[-1].split(".")
    return name[0] + "_color." + name[1]

class algo_client():
    def __init__(self, apiKey, model_name, local_dir="data/", cloud_in_dir="data://.my/data_in/"):
        self.client = Algorithmia.client(apiKey)
        self.algo = self.client.algo(model_name)

        self.local_dir = local_dir
        self.cloud_in_dir = cloud_in_dir

    def colorize(self, img_name):
        #загрузка файла на сайт
        self.client.file(self.cloud_in_dir + img_name).putFile(self.local_dir + img_name)

        #раскраска
        input = {"image": self.cloud_in_dir + img_name}
        cloud_color_img = self.algo.pipe(input).result['output']

        #загрузка файла с сайта
        color_file = self.client.file(cloud_color_img).getBytes()

        #запись в файл
        color_img_name = get_color_name(cloud_color_img)
        with open(self.local_dir + color_img_name, "wb") as f:
            f.write(color_file)





if __name__ == '__main__':
    client = algo_client(apiKey='simIVvEvW9njMmOIYwAtYFdxtFe1',
                         model_name='deeplearning/ColorfulImageColorization/1.1.13',
                         local_dir="data/",
                         cloud_in_dir="data://.my/data_in/")

    img_name = sys.argv[1]
    client.colorize(img_name)
    print("Done")