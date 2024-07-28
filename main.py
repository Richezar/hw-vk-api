import configparser
import VKdownloader
import YAuploader

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('token.ini')
    user_id = str(input('Введите id пользователя VK: '))
    vk = VKdownloader.VKdownloader(config['VK']['token'], user_id)
    print(vk.users_info())

    ya = YAuploader.YAuploader(config['YA']['token'])
    folder_name = f'vk_{user_id}'
    ya.create_folder(folder_name)
    ya.upload_folder(folder_name, vk.download_all_photos())