import bs4 as bs4
import requests

import stage
import pnconnector

class VkBot:
    def __init__(self, user_id):
        self._short_list_len_limit = 101
        self._stage = stage.Stage.START

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
            if 0 < int(message) and int(message) < self._short_list_len_limit:
                self._stage = stage.Stage.TEXT_IS_READY
        except:
            if 'ДАЛЕЕ' in message.upper():
                self._stage = stage.Stage.WHAITING_CHOSE_HERO
            elif 'НЕТ' in message.upper():
                self._stage = stage.Stage.HERO_NOT_FOUND
    
    def _load_photo_or_post_text(self, message):
        if 'ДА' in message.upper() or 'ЕСТЬ' in message.upper():
            self._stage = stage.Stage.WHAITING_PHOTO
        
        else:
            self._stage = stage.Stage.POST_IS_READY


    def new_message(self, message):

        if self._stage is stage.Stage.START:
            self._stage = stage.Stage.WHAITING_NAME
            return f'Привет, {self._USERNAME}! Я помогу тебе найти героя по имени и сгенерирую пост. \n\nВведи имя героя.'
        
        elif self._stage is stage.Stage.WHAITING_NAME:
            self._stage = stage.Stage.WHAITING_CHOSE_HERO
            pnc = pnconnector.PNConnector()
            self._items = pnc.getData(message, self._short_list_len_limit)
            count = int(len(self._items))
            text = self._items_short_list()
            return f'Мне удалось найти более {count} людей. Вот список героев ВОВ которых я нашел:\n{text}\nМне удалось найти твоего героя или ищем дальше?\n\nОтветьте: номером из списка или нет - если человек не найден.'


        if self._stage is stage.Stage.WHAITING_CHOSE_HERO:
            self._search_continue_or_next_stage(message)
        
        # if self._stage is stage.Stage.WHAITING_CHOSE_HERO:
        #     count = 10
        #     return f'Мне удалось найти {count} людей. Вот список героев ВОВ которых я нашел: ... Мне удалось найти твоего героя или ищем дальше?'
        
        # Забываем все остальные записи
        self._items = []


        if self._stage is stage.Stage.HERO_NOT_FOUND:
            self._stage = stage.Stage.START
            return f'Мне очень жаль. Нужно уточнить поиск. Попробуй еще раз.'

        if self._stage is stage.Stage.TEXT_IS_READY:
            self._stage = stage.Stage.WHAITING_PHOTO
            post_text = 'Содержание поста'
            return f'Вот такой пост мы подготовили:\n\n{post_text}\n\nПост почти готов! Если у вас есть фото, то люди будут знать героя в лицо! Вы хотите добавить фото?\n\nОтветьте да или нет'


        if self._stage is stage.Stage.WHAITING_PHOTO:
            self._load_photo_or_post_text(message)


        if self._stage is stage.Stage.WHAITING_PHOTO:
            self._stage = stage.Stage.START
            return f'Отлично! Жду фото с героем ВОВ :)'

        elif self._stage is stage.Stage.POST_IS_READY:
            self._stage = stage.Stage.START
            return f'Пост готов! Давайте его опубликуем?\n\n(кнопка/ссылка опубликовать)'

        
        return 'Не понимаю о чем вы...'

    def _get_time(self):
        request = requests.get('https://my-calend.ru/date-and-time-today')
        b = bs4.BeautifulSoup(request.text, 'html.parser')
        return self._clean_all_tag_from_str(str(b.select('.page')[0].findAll('h2')[1])).split()[1]

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