from time import sleep

from imageprocessing.colorization import AlgoClient
from imageprocessing.validation import KerasValidationModel

class AlgoManager():
    # {"user_id": {"status": "wait", "file": "file_name.jpg"}}
    _tasks = {}

    def __init__(self, config: dict, tasks_boffer: dict):
        path = config['IMAGES_DIR']
        self._tasks_boffer = tasks_boffer
        self._algoclient = AlgoClient(local_dir=path + '/')

    def process(self):
        while True:
            try:
                for user_id, task in self._tasks_boffer.items():
                    if task['status'] == 'wait':
                        file_name = task['file'].split('/')[-1]
                        print(f'AlgoManager: colorize ({user_id}) - started')
                        color_img_path = self._algoclient.colorize(file_name)
                        print(f'AlgoManager: colorize ({user_id}) - finished')
                        task['file'] = color_img_path
                        task['status'] = 'ready'
                        self._tasks_boffer[user_id] = task
            except Exception as e:
                print('Error: ' + str(e))
            sleep(0.1)