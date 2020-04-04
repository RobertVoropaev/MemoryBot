import requests
import json

class PNConnector:
    def __init__(self):
        pass

    def getData(self, name='', page=0):
        if not name:
            return []

        url = 'https://foto.pamyat-naroda.ru/api/hero?search='
        url += name

        if page:
            url += f'&page={page}' 
        
        req = requests.get(url)
        return json.loads(req.text)['items']