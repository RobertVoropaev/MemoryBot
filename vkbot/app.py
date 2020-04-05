import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from VkBot import VkBot


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
    

token = "206a6ee2c7c2c10793de804210350d8b9dc055f467f5d1a8a231e554ef9b9326be70216ab5e6a8c084f3a"
# KM
# token = "52def8326ae174c1963079e5d9c9dda0fcf1f0b77a9d999abe2382fa8cc30dd5d0d4b6f5cc823ae454471"


vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)

print("Server started")

bots = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print(f'Recive from {event.user_id}: {event.text}')

            bot = None
            if event.user_id not in bots:
                bot = VkBot(event.user_id)
                bots[event.user_id] = bot
            else:
                bot = bots[event.user_id]

            write_msg(event.user_id, bot.new_message(event.text))