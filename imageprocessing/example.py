from colorization import AlgoClient
from validation import KerasValidationModel


############ Модуль колоризации ############

# сюда нужно передать путь до папки, в которой будут лежать фотографии
algoclient = AlgoClient(local_dir="data/")

img_name = "1.jpg"
# получает на вход имя файла в папке
color_img_path = algoclient.colorize(img_name)
# возвращает имя цветного файла в этой же папке
print(color_img_path) # 1234_color.jpg


############ Модуль валидации ############

# сюда нужно передать путь до папки, в которой будут лежать фотографии
keras_model = KerasValidationModel(local_dir="data/")

img_name = "1.jpg"

# получает на вход имя файла в папке и возвращает True, если фотка валидна
result = keras_model.is_valid_photo(img_name)

if result:
    print('Valid')
else:
    print('No valid')