from dask.bytes.tests.test_http import requests
import random


def get_photo_by_url(photo_url):
    photo = requests.get(photo_url)
    photo_file = open(f'../data/{random.randint(0, 2048)}.png', "wb")
    photo_file.write(photo.content)
    photo_file.close()


def get_photo_from_message(vk, id):
    return vk.method('messages.getById', {'message_ids': id})['items'][0]['attachments']


def write_msg(vk, user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
