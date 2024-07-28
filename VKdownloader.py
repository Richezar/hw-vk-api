import requests
import json


class VKdownloader:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_common_params(self):  # основные параметры
        return {
            'access_token': self.token,
            'v': self.version
        }

    def users_info(self):  # информация о пользователе
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_id_user(self):
        return self.users_info()['response'][0]['id']

    def get_profile_photos(self):  # в этом методе на выходе имеем json файл с данными о всех фотографиях пользователя
        url = 'https://api.vk.com/method/photos.get'
        params = self.get_common_params()
        params.update({'owner_id': self.get_id_user(),
                       'album_id': 'profile',
                       'rev': 0,
                       'extended': 1,
                       'photo_sizes': 1
                       })
        response = requests.get(f'{url}', params=params)
        return response.json()

    def get_all_photos(self):
        data = self.get_profile_photos()
        all_name_url_photo = {}  # словарь {name : url},
        info_photo = []  # данные о полученных фото, размер, имя фото - лайки(дата если одинаковое кол-во)
        count_photo = data['response']['count']  # кол-во фото
        for i in range(count_photo):
            count_likes = data['response']['items'][i]['likes']['count']  # кол-во лайков
            url_photo = ''
            tmp_height = 0  # размер, который будет записываться в список
            tmp_width = 0  # размер, который будет записываться в список
            photo_info = {}
            for j in data['response']['items'][i]['sizes']:
                # выбираем самый максимальный размер и сохраняем его вместе с url
                if j['height'] > tmp_height:
                    tmp_height = j['height']
                    tmp_width = j['width']
                    url_photo = j['url']

            if count_likes not in all_name_url_photo:  # если лайк не повторяется, записываем в формате лайки.jpg
                all_name_url_photo[count_likes] = url_photo
                photo_info['file_name'] = f'{count_likes}.jpg'
            else:  # если лайк повторяется, записываем в формате лайки_дата.jpg
                data_photo = data['response']['items'][i]['date']
                all_name_url_photo[str(count_likes) + '_' + str(data_photo)] = url_photo
                photo_info['file_name'] = f'{str(count_likes)}_{str(data_photo)}.jpg'
            photo_info['sizes'] = f'{tmp_height}x{tmp_width}'
            info_photo.append(photo_info)
        return all_name_url_photo, info_photo

    def download_all_photos(self):
        # получение словаря и итогового файла с информацией о скаченных фото
        # {file_name : имя} и {sizes : размер}
        data, info_photo = self.get_all_photos()
        with open("info_photo.json", "w") as file:  # загрузка файла с информацией о фото
            json.dump(info_photo, file, indent=10)
        return data
