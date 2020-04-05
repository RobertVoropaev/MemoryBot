import numpy as np
import keras
import sys

from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions

class ValidationModel:
    def __init__(self, local_dir="data/", models_dir="models/"):
        self.model = keras.models.load_model(models_dir + 'model.h5')

        self.valid_classes = ['military_uniform', 'pickelhaube', 'web_site', 'bow_tie', 'academic_gown',
                            'suit', 'mortarboard', 'accordion', 'sunglass', 'Windsor_tie']

        self.top_num = 3
        self.local_dir = local_dir

    def is_valid_photo(self, img_name):
        img_path = self.local_dir + img_name

        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        predictions = decode_predictions(self.model.predict(x), top=self.top_num)[0]
        predictions = list(map(lambda x: x[1], predictions))

        for pred in predictions:
            if pred in self.valid_classes:
                return True
        return False



if __name__ == '__main__':
    # сюда нужно передать путь до папки, в которой будут лежать фотографии, и путь до модели
    validation_model = ValidationModel(local_dir="data/", models_dir="models/")

    img_name = sys.argv[1]

    #получает на вход имя файла в папке и возвращает True, если фотка валидна
    result = validation_model.is_valid_photo(img_name)

    if result:
        print('Valid')
    else:
        print('No valid')
