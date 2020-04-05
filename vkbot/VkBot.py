import bs4 as bs4
import requests
from time import sleep

import stage
import pnconnector
from vk_api import vk_api
from vk_api import VkUpload

from imageprocessing.colorization import AlgoClient
from imageprocessing.validation import KerasValidationModel


class VkBot:
    def __init__(self, user_id: int, config: dict, algomanager_tasks: dict):
        self._short_list_len_limit = 101
        self._stage = stage.Stage.START

        self._algomanager_tasks = algomanager_tasks
        self._config = config

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

    @property
    def stage(self):
        return self._stage

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get('https://vk.com/id' + str(user_id))
        bs = bs4.BeautifulSoup(request.text, 'html.parser')

        user_name = self._clean_all_tag_from_str(bs.findAll('title')[0])

        return user_name.split()[0]

    def _search_continue_or_next_stage(self, message):
        try:
            value = int(message)
            if 0 < value and value <= self._short_list_len_limit:
                ind = value - 1
                self._pn_item = self._items[ind]
                self._items = []
                self._stage = stage.Stage.TEXT_IS_READY
        except:
            if 'ДАЛЕЕ' in message.upper():
                self._stage = stage.Stage.WHAITING_CHOSE_HERO
            elif 'НЕТ' in message.upper():
                self._stage = stage.Stage.HERO_NOT_FOUND
    
    def _load_photo_or_post_text(self, message):
        if 'ДА' in message.upper() or 'ЕСТЬ' in message.upper():
            self._stage = stage.Stage.DO_YOU_HAVE_PHOTO
        
        else:
            self._stage = stage.Stage.POST_IS_READY

    def _build_post_text(self):
        data = self._pn_item
        text = ''
        if data['Rank']:
            text += '%s ' % data['Rank']
        if data['Lastname']:
            text += '%s ' % data['Lastname']
        if data['Firstname']:
            text += '%s ' % data['Firstname']
        if data['Patronymic']:
            text += '%s ' % data['Patronymic']
        if data['Birthday']:
            text += 'родился %s' % data['Birthday']
        text += '.\n'
        
        if data['Unit']:
            text += 'Во время войны служил в %s,' % data['Unit']
        if data['Callplace']:
            text += '%s ' % data['Callplace']
        if data['Calldate']:
            text += '%s' % data['Calldate']
        text += '.\n'

        if 'sourcelink' in data:
            text += 'О наградах можно почитать здесь %s.\n' % data['sourcelink']
            
        text += 'Я помню.\n\n#бессмертныйполконлайн #memorybot #дорогапамяти'

        self._post_text = text

    def _get_photo_by_url(self, photo_url):
        photo = requests.get(photo_url)
        file_name = photo_url.split('/')[-1]
        photo_file = open('%s/%s' % (self._config['IMAGES_DIR'], file_name), "wb")
        photo_file.write(photo.content)
        photo_file.close()

    def _get_photo_from_message(self, message_id, api):
        photos = api.method('messages.getById', {'message_ids': message_id})['items'][0]['attachments']
        return photos[0]['photo']['sizes'][4]['url']

    def _get_vk_photo_from_local(self, image_path):
        vk = vk_api.VkApi(self._config['APP_KEY'])
        # upload_url = vk.method('photos.getUploadServer', {'album_id':270364396, 'group_id':193773037})
        # print(upload_url)
        upload = VkUpload(vk)
        photo = upload.photo(  # Подставьте свои данные
            image_path,
            album_id=270364396,
            group_id=193773037
        )
        photo = photo[0]
        owner_id = photo['owner_id']
        photo_id = photo['id']
        return f'photo{owner_id}_{photo_id}'

    def _post_to_community(self, message, image_path=""):
        vk = vk_api.VkApi(self._config['APP_KEY'])
        if image_path!="":
            photo_url = self._get_vk_photo_from_local(image_path)
            vk.method('wall.post', {'owner_id':-193773037, 'from_group':1, "message":message, 'attachments': photo_url})
        else:
            vk.method('wall.post', {'owner_id': -193773037, 'from_group': 1, "message": message
                                })

    def new_message(self, message, message_id, api):

        if self._stage is stage.Stage.START:
            self._stage = stage.Stage.WHAITING_NAME
            return {
                'm': f'Привет, {self._USERNAME}! Я помогу тебе найти героя по имени и сгенерирую пост. \n\n' \
                    'Введи имя и героя и год рождения (если известен). Примеры: \n\n' \
                    'Иванов Алексей 1915\n' \
                    'Смирнов Василий\n' \
                    'Воронухин\n',
                'att': ''
            }
        
        elif self._stage is stage.Stage.WHAITING_NAME:
            self._stage = stage.Stage.WHAITING_CHOSE_HERO

            def parse_query(q: str):
                last_four = q[-4:]
                if len(last_four) == 4 and last_four.isnumeric():
                    date = last_four
                    return q[:-4].strip(), date
                else:
                    return q, None
            name, date = parse_query(message.strip())
            print(f'Parsed query: name: {name}, birth_year: {date}')
            pnc = pnconnector.PNConnector()
            self._items = pnc.getData(name, date, self._short_list_len_limit)
            count = int(len(self._items))
            text = self._items_short_list()
            return {'m': f'Мне удалось найти более {count} людей. Вот список героев ВОВ которых я нашел:\n' \
                        f'{text}\n'
                        'Мне удалось найти твоего героя или ищем дальше?\n\n' \
                        'Ответьте: номером из списка или нет - если человек не найден.',
                    'att': ''}

        if self._stage is stage.Stage.WHAITING_CHOSE_HERO:
            self._search_continue_or_next_stage(message)
        
        # if self._stage is stage.Stage.WHAITING_CHOSE_HERO:
        #     count = 10
        #     return f'Мне удалось найти {count} людей. Вот список героев ВОВ которых я нашел: ... Мне удалось найти твоего героя или ищем дальше?'
        
        # Забываем все остальные записи
        self._items = []

        if self._stage is stage.Stage.HERO_NOT_FOUND:
            self._stage = stage.Stage.START
            return {'m':f'Мне очень жаль. Нужно уточнить поиск. Попробуй еще раз.',
                    'att': ''}

        if self._stage is stage.Stage.TEXT_IS_READY:
            self._stage = stage.Stage.DO_YOU_HAVE_PHOTO
            self._build_post_text()
            return {'m': f'Вот такой пост мы подготовили:\n\n' \
                        f'{self._post_text}\n\n' \
                        'Пост почти готов! Если у вас есть фото, то люди будут знать героя в лицо! Вы хотите добавить фото?\n\n' \
                        'Ответьте да или нет',
                    'att': ''}


        if self._stage is stage.Stage.DO_YOU_HAVE_PHOTO:
            self._load_photo_or_post_text(message)


        if self._stage is stage.Stage.DO_YOU_HAVE_PHOTO:
            self._stage = stage.Stage.WHAITING_PHOTO
            return {'m':f'Отлично! Жду фото с героем ВОВ :)',
                    'att':''}

        if self._stage is stage.Stage.WHAITING_PHOTO:
            photo = self._get_photo_from_message(message_id, api)
            self._get_photo_by_url(photo)

            # self._stage = stage.Stage.START
            file_name = photo.split('/')[-1]
            path = '%s/%s' % (self._config['IMAGES_DIR'], file_name)
            self._algomanager_tasks[self._USER_ID] = {'status': 'wait', 'file': path}
            time_out = self._config['ALGOMANAGER_TIMEOUT']

            path = ''
            while time_out > 0:
                for user_id, task in self._algomanager_tasks.items():
                    if user_id == self._USER_ID:
                        if task['status'] == 'ready':
                            path = task['file']
                            self._algomanager_tasks.pop(user_id)
                            break
                if path:
                    break

                time_out -= 1
                sleep(1)
            self._post_to_community("Пост", self._get_vk_photo_from_local(path))
            return {'m': f'Пост готов! \n\n' \
                        f'(фото {path})\n\n' \
                        f'{self._post_text}\n\n' \
                        'Давайте его опубликуем?\n\n' \
                        '(кнопка/ссылка опубликовать)',
                    'att': self._get_vk_photo_from_local(path)}

        elif self._stage is stage.Stage.POST_IS_READY:
            self._stage = stage.Stage.START
            return {'m': 'Пост готов! Давайте его опубликуем?\n\n' \
                        '(кнопка/ссылка опубликовать)',
                    'att': ''}

        self._stage = stage.Stage.START
        return {'m':'Не понимаю о чем вы...', 'att': ''}

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        '''
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        '''

        result = ''
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == '<':
                    not_skip = False
                else:
                    result += i
            else:
                if i == '>':
                    not_skip = True

        return result

    def _items_short_list(self):
        text = ''
        for index, item in enumerate(self._items):
            text += '%i: %s %s %s\n' % (index + 1, item['Firstname'], item['Lastname'], item['Patronymic'])

        return text
