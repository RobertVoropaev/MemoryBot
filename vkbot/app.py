import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from VkBot import VkBot


def write_msg(user_id, message, att):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048), 'attachments':att})
    
import json
import sys

CONFIG_FILE = 'config.json'
config = None

with open(CONFIG_FILE) as json_file:
    config = json.load(json_file)

keys = {'KEY', 'IMAGES_DIR'}

for key in keys:
    if key not in config:
        print('Error: incorrect %s file: %s key is missing' % (CONFIG_FILE, key))
        sys.exit()

token = config['KEY']

vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)

import threading
from algomanager import AlgoManager

algomanager_tasks = {}
algomanager = AlgoManager(config, algomanager_tasks)
algomanager_thread = threading.Thread(target=algomanager.process)
algomanager_thread.start()

print("Server started")

bots = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print(f'Recive from {event.user_id}: {event.text}')
            bot = None
            if event.user_id not in bots:
                bot = VkBot(event.user_id, config, algomanager_tasks)
                bots[event.user_id] = bot
            else:
                bot = bots[event.user_id]
            print(event.text)
            message = bot.new_message(event.text, event.message_id, vk)
            print(message)
            write_msg(event.user_id, message['m'], message['att'])
