import requests


class YAuploader:
    def __init__(self, token):
        self.token = token

    def create_folder(self, folder):  # метод создает папку на Я.Диск
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {
            'path': folder
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }
        requests.put(url, params=params, headers=headers)

    def upload_folder(self, name_folder, name_url):  # метод загружает фото по заданному пути в Я.Диск
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        count = 0
        for k, v in name_url.items():
            params = {
                'path': f'{name_folder}/{k}',
                'url': v
            }
            headers = {
                'Authorization': f'OAuth {self.token}'
            }
            requests.post(url, params=params, headers=headers)
            count += 1
            print(f'Загружено {count} фото из {len(name_url)}')