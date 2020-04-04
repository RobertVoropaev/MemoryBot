import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from VkBot import VkBot


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


token = "206a6ee2c7c2c10793de804210350d8b9dc055f467f5d1a8a231e554ef9b9326be70216ab5e6a8c084f3a"


vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)

print("Server started")
print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('New message:')
            print(f'For me by: {event.user_id}', end='')

            bot = VkBot(event.user_id)
            write_msg(event.user_id, bot.new_message(event.text))

            print('Text: ', event.text)
