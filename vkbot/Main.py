

import vk_api
from .util import get_photo_by_url, get_photo_from_message, write_msg
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

from .VkBot import VkBot

token = "206a6ee2c7c2c10793de804210350d8b9dc055f467f5d1a8a231e554ef9b9326be70216ab5e6a8c084f3a"

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)
upload = VkUpload(vk)  # Для загрузки изображений

print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        bot = VkBot(event.user_id)
        photos = get_photo_from_message(vk, event.message_id)

        if 1 < len(photos):
            write_msg(vk, event.user_id, bot.new_message("Пришлите, пожалуйста, только одну фотографию."))
        else:
            photo_url = photos[0]['photo']['sizes'][4]['url']
            get_photo_by_url(photo_url)

        write_msg(vk, event.user_id, bot.new_message(event.text))

