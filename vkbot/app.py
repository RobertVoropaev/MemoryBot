import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from VkBot import VkBot


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
    
import json
import sys

CONFIG_FILE = 'config.json'
config = None

with open(CONFIG_FILE) as json_file:
    config = json.load(json_file)

keys = {'KEY'}

for key in keys:
    if key not in config:
        print('Error: incorrect %s file: %s key is missing' % (CONFIG_FILE, key))
        sys.exit()

token = config['KEY']

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