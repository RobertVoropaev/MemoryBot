from colorization import ColorizeModel
from validation import ValidationModel
from denoizing import DenoizeModel


############ Модуль валидации ############

# сюда нужно передать путь до папки, в которой будут лежать фотографии и путь до папки с моделью (model.h5)
validation_model = ValidationModel(local_dir="data/", models_dir="models/")

img_name = "3.jpg"

# получает на вход имя файла в папке и возвращает True, если фотка валидна
result = validation_model.is_valid_photo(img_name)

if result:
    print('Valid')
else:
    print('No valid')

############ Модуль шумоподавления ############

# сюда нужно передать путь до папки, в которой будут лежать фотографии
denoize_model = DenoizeModel(local_dir="data/")

img_name = "3.jpg"
# получает на вход имя файла в папке, сохраняет в ту же папку фото без шума и возвращает его имя
denoize_img_name = denoize_model.denoizing(img_name)

print(denoize_img_name)

############ Модуль колоризации ############

# сюда нужно передать путь до папки, в которой будут лежать фотографии
colorize_model = ColorizeModel(local_dir="data/")

img_name = "3_denoize.jpg"
# получает на вход имя файла в папке
color_img_path = colorize_model.colorize(img_name)
# возвращает имя цветного файла в этой же папке
print(color_img_path) # 1234_color.jpg




