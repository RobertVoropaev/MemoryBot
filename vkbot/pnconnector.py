import requests
import json
from time import sleep

class PNConnector:
    def __init__(self):
        pass

    def getData(self, name: str, limit=100):
        page = 1
        items = []

        while len(items) < limit:
            data = self._get_data_by_page(name, page)
            if not data:
                break
            items.extend(data['items'])
            print('items len: ' + str(len(items)))
            page += 1
            # Без sleep api перестает отдавать данные после 200 записи
            # sleep(1.5)
        
        return items[:limit - 1]

    def _get_data_by_page(self, name: str, page: int):
        if not name:
            return []

        url = 'https://foto.pamyat-naroda.ru/api/hero?search='
        url += name
        url += f'&page={page}'

        data = {}
        try:
            req = requests.get(url)
            if req.status_code == 200:
                data = json.loads(req.text)
        except requests.exceptions.Timeout:
            print('Timeout')
        except requests.exceptions.RequestException as e :
            print(str(e))
        except Exception as e:
            print(str(e))
            
        return data
        