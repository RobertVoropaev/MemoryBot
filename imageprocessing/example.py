from colorization import AlgoClient

# сюда нужно передать путь до папки, в которой будут лежать фотографии
algoclient = AlgoClient(local_dir="data/")

img_name = "1234.jpg"
# получает на вход имя файла в папке
color_img_path = algoclient.colorize(img_name)
# возвращает имя цветного файла в этой же папке
print(color_img_path) # 1234_color.jpg